"""Стиснення зображень з адмінки у WebP перед записом у media/."""

from dataclasses import dataclass, field
from io import BytesIO
from pathlib import PurePosixPath

from django.core.exceptions import SuspiciousFileOperation, ValidationError
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import transaction
from django.db.models.signals import post_save, pre_save
from django.utils.text import get_valid_filename
from PIL import Image, ImageOps, UnidentifiedImageError

from src.core.image_specs import (
    BLOG_COVER_LIMIT,
    FLOOR_PLAN_LIMIT,
    GALLERY_LIMIT,
    MODEL_IMAGE_LIMIT,
    TEAM_PHOTO_LIMIT,
    ImageLimit,
)

_FIELD_LIMITS: dict | None = None
_SIGNALS_CONNECTED = False


@dataclass
class FieldCompressResult:
    converted: bool = False
    previous_name: str = ''


@dataclass
class CompressStats:
    converted: int = 0
    skipped: int = 0
    missing: int = 0
    errors: list[str] = field(default_factory=list)
    changes: list[str] = field(default_factory=list)


def field_limits() -> dict:
    global _FIELD_LIMITS
    if _FIELD_LIMITS is None:
        from src.blog.models import Post
        from src.catalog.models import DomeModel, ModelImage
        from src.gallery.models import GalleryPhoto
        from src.pages.models import TeamMember

        _FIELD_LIMITS = {
            DomeModel: {'floor_plan_image': FLOOR_PLAN_LIMIT},
            ModelImage: {'image': MODEL_IMAGE_LIMIT},
            Post: {'cover_image': BLOG_COVER_LIMIT},
            GalleryPhoto: {'image': GALLERY_LIMIT},
            TeamMember: {'photo': TEAM_PHOTO_LIMIT},
        }
    return _FIELD_LIMITS


def connect_image_compress_signals():
    global _SIGNALS_CONNECTED
    if _SIGNALS_CONNECTED:
        return
    pre_save.connect(compress_on_pre_save, dispatch_uid='core.compress_images_pre')
    post_save.connect(cleanup_replaced_images, dispatch_uid='core.compress_images_post')
    _SIGNALS_CONNECTED = True


def disconnect_image_compress_signals():
    global _SIGNALS_CONNECTED
    pre_save.disconnect(dispatch_uid='core.compress_images_pre')
    post_save.disconnect(dispatch_uid='core.compress_images_post')
    _SIGNALS_CONNECTED = False


def encode_webp(raw: bytes, limit: ImageLimit) -> bytes:
    if not raw:
        raise ValidationError('Порожній файл зображення.')
    try:
        with Image.open(BytesIO(raw)) as opened:
            if getattr(opened, 'is_animated', False):
                opened.seek(0)
            image = ImageOps.exif_transpose(opened)
            image = _to_web_mode(image)
            if image.width > limit.max_width or image.height > limit.max_height:
                image.thumbnail(
                    (limit.max_width, limit.max_height),
                    Image.Resampling.LANCZOS,
                )
            buffer = BytesIO()
            image.save(buffer, format='WEBP', quality=limit.quality, method=6)
            return buffer.getvalue()
    except (UnidentifiedImageError, Image.DecompressionBombError, OSError) as exc:
        raise ValidationError('Файл не є зображенням JPG, PNG або WebP.') from exc


def compress_field(instance, field_name: str, limit: ImageLimit, *, force: bool = False) -> FieldCompressResult:
    field_file = getattr(instance, field_name, None)
    if not field_file or not getattr(field_file, 'name', None):
        return FieldCompressResult()

    committed = getattr(field_file, '_committed', True)
    if committed and not force:
        return FieldCompressResult()

    if committed:
        if not default_storage.exists(field_file.name):
            raise FileNotFoundError(field_file.name)
        raw = _read_image_bytes(field_file)
        if not _bytes_need_compress(field_file.name, raw, limit):
            return FieldCompressResult()
        previous = field_file.name
    else:
        previous = _stored_name(instance, field_name)
        raw = _read_image_bytes(field_file)

    payload = encode_webp(raw, limit)
    field_file.save(webp_filename(field_file.name), ContentFile(payload), save=False)
    if previous and previous != field_file.name:
        return FieldCompressResult(converted=True, previous_name=previous)
    return FieldCompressResult(converted=True)


def compress_saved_media() -> CompressStats:
    """Конвертує вже збережені файли моделей. WebP у межах ліміту не перестискається."""
    stats = CompressStats()
    for model, fields in field_limits().items():
        for instance in model.objects.all().iterator():
            changed_fields: list[str] = []
            pending_delete: list[str] = []
            for field_name, limit in fields.items():
                label = f'{model.__name__} #{instance.pk} {field_name}'
                field_file = getattr(instance, field_name, None)
                if not field_file or not field_file.name:
                    stats.skipped += 1
                    continue
                try:
                    result = compress_field(instance, field_name, limit, force=True)
                except FileNotFoundError:
                    stats.missing += 1
                    stats.errors.append(f'{label}: немає файлу {field_file.name}')
                    continue
                except ValidationError as exc:
                    stats.errors.append(f'{label}: {exc.messages[0]}')
                    continue
                if not result.converted:
                    stats.skipped += 1
                    continue
                stats.converted += 1
                new_name = getattr(instance, field_name).name
                stats.changes.append(f'{result.previous_name or new_name} → {new_name}')
                if result.previous_name:
                    pending_delete.append(result.previous_name)
                changed_fields.append(field_name)
            if not changed_fields:
                continue
            with transaction.atomic():
                instance.save(update_fields=changed_fields)
            for name in pending_delete:
                if default_storage.exists(name):
                    default_storage.delete(name)
    return stats


def compress_on_pre_save(sender, instance, **kwargs):
    limits = field_limits().get(sender)
    if not limits:
        return
    stale: list[str] = []
    for field_name, limit in limits.items():
        result = compress_field(instance, field_name, limit, force=False)
        if result.previous_name:
            stale.append(result.previous_name)
    if stale:
        instance._image_compress_cleanup = stale


def cleanup_replaced_images(sender, instance, **kwargs):
    if sender not in field_limits():
        return
    names = getattr(instance, '_image_compress_cleanup', None)
    if not names:
        return
    for name in names:
        if name and default_storage.exists(name):
            default_storage.delete(name)
    instance._image_compress_cleanup = []


def webp_filename(original_name: str) -> str:
    stem = PurePosixPath(original_name or 'image').stem or 'image'
    try:
        safe = get_valid_filename(stem)
    except SuspiciousFileOperation:
        safe = 'image'
    return f'{(safe or "image")[:60]}.webp'


def _to_web_mode(image: Image.Image) -> Image.Image:
    if image.mode in ('RGB', 'RGBA'):
        return image
    if image.mode in ('P', 'PA', 'LA') and ('transparency' in image.info or image.mode != 'P'):
        return image.convert('RGBA')
    return image.convert('RGB')


def _bytes_need_compress(name: str, raw: bytes, limit: ImageLimit) -> bool:
    if not name.lower().endswith('.webp'):
        return True
    with Image.open(BytesIO(raw)) as image:
        return image.width > limit.max_width or image.height > limit.max_height


def _read_image_bytes(field_file) -> bytes:
    if not getattr(field_file, '_committed', True):
        source = field_file.file
        source.seek(0)
        data = source.read()
        source.seek(0)
        return data
    with field_file.open('rb') as handle:
        return handle.read()


def _stored_name(instance, field_name: str) -> str:
    if not instance.pk:
        return ''
    value = (
        instance.__class__.objects.filter(pk=instance.pk)
        .values_list(field_name, flat=True)
        .first()
    )
    return value or ''
