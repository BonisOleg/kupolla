from io import BytesIO

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from PIL import Image

from src.catalog.models import DomeModel, ModelImage
from src.core.image_compress import (
    compress_saved_media,
    connect_image_compress_signals,
    disconnect_image_compress_signals,
)
from src.gallery.models import GalleryPhoto
from src.pages.models import TeamMember


def _upload(name: str, image: Image.Image, fmt: str) -> SimpleUploadedFile:
    buffer = BytesIO()
    save_kwargs = {'format': fmt}
    if fmt == 'JPEG':
        save_kwargs['exif'] = image.getexif()
    image.save(buffer, **save_kwargs)
    content_type = 'image/jpeg' if fmt == 'JPEG' else 'image/png'
    return SimpleUploadedFile(name, buffer.getvalue(), content_type=content_type)


def _dome() -> DomeModel:
    return DomeModel.objects.create(name='Тест', area_m2=35, diameter='6.0', height_m='3.5')


class ImageCompressTests(TestCase):
    def test_png_upload_becomes_resized_webp(self):
        image = ModelImage.objects.create(
            dome=_dome(),
            image=_upload('wide.png', Image.new('RGB', (2400, 1200), (20, 40, 60)), 'PNG'),
            alt='фасад',
        )
        self.assertTrue(image.image.name.endswith('.webp'))
        with Image.open(image.image.path) as saved:
            self.assertEqual(saved.format, 'WEBP')
            self.assertLessEqual(saved.width, 1600)
            self.assertLessEqual(saved.height, 1600)
            self.assertEqual(saved.size, (1600, 800))

    def test_resave_keeps_the_same_file(self):
        image = ModelImage.objects.create(
            dome=_dome(),
            image=_upload('photo.png', Image.new('RGB', (400, 300), (10, 10, 10)), 'PNG'),
        )
        name = image.image.name
        payload = image.image.read()
        image.alt = 'оновлений alt'
        image.save()
        image.refresh_from_db()
        self.assertEqual(image.image.name, name)
        self.assertEqual(image.image.read(), payload)

    def test_png_alpha_stays_transparent(self):
        image = ModelImage.objects.create(
            dome=_dome(),
            image=_upload('plan.png', Image.new('RGBA', (120, 80), (255, 0, 0, 0)), 'PNG'),
        )
        with Image.open(image.image.path) as saved:
            self.assertEqual(saved.mode, 'RGBA')
            self.assertEqual(saved.getpixel((0, 0))[3], 0)

    def test_exif_orientation_is_applied(self):
        source = Image.new('RGB', (90, 30), (200, 0, 0))
        source.getexif()[274] = 6
        image = ModelImage.objects.create(
            dome=_dome(),
            image=_upload('rotated.jpg', source, 'JPEG'),
        )
        with Image.open(image.image.path) as saved:
            self.assertEqual(saved.size, (30, 90))

    def test_replacing_image_deletes_the_previous_file(self):
        image = ModelImage.objects.create(
            dome=_dome(),
            image=_upload('first.png', Image.new('RGB', (80, 80), (1, 2, 3)), 'PNG'),
        )
        previous = image.image.name
        image.image = _upload('second.png', Image.new('RGB', (80, 80), (4, 5, 6)), 'PNG')
        image.save()
        image.refresh_from_db()
        self.assertNotEqual(image.image.name, previous)
        self.assertFalse(default_storage.exists(previous))

    def test_assigned_webp_is_not_reencoded(self):
        payload = BytesIO()
        Image.new('RGB', (40, 40), (7, 8, 9)).save(payload, format='WEBP', quality=80)
        raw = payload.getvalue()
        path = default_storage.save('catalog/already.webp', ContentFile(raw))
        image = ModelImage(dome=_dome(), alt='seed')
        image.image.name = path
        image.save()
        self.assertEqual(image.image.name, path)
        with default_storage.open(path, 'rb') as handle:
            self.assertEqual(handle.read(), raw)

    def test_team_photo_is_capped_at_800(self):
        member = TeamMember.objects.create(
            name='Олена Коваль',
            position='Архітектор',
            photo=_upload('face.png', Image.new('RGB', (1200, 900), (30, 30, 30)), 'PNG'),
        )
        with Image.open(member.photo.path) as saved:
            self.assertEqual(saved.format, 'WEBP')
            self.assertLessEqual(max(saved.size), 800)

    def test_command_converts_existing_jpeg_and_skips_webp(self):
        disconnect_image_compress_signals()
        try:
            jpeg = BytesIO()
            Image.new('RGB', (100, 60), (12, 12, 12)).save(jpeg, format='JPEG')
            photo = GalleryPhoto(title='старе')
            photo.image.save('legacy.jpg', ContentFile(jpeg.getvalue()), save=True)
            legacy_name = photo.image.name
        finally:
            connect_image_compress_signals()

        webp = BytesIO()
        Image.new('RGB', (50, 50), (1, 1, 1)).save(webp, format='WEBP', quality=80)
        kept = GalleryPhoto(title='готове')
        kept.image.name = default_storage.save('gallery/kept.webp', ContentFile(webp.getvalue()))
        kept.save()
        kept_name = kept.image.name
        kept_bytes = default_storage.open(kept_name, 'rb').read()

        stats = compress_saved_media()

        photo.refresh_from_db()
        kept.refresh_from_db()
        self.assertTrue(photo.image.name.endswith('.webp'))
        self.assertFalse(default_storage.exists(legacy_name))
        self.assertEqual(kept.image.name, kept_name)
        with default_storage.open(kept_name, 'rb') as handle:
            self.assertEqual(handle.read(), kept_bytes)
        self.assertGreaterEqual(stats.converted, 1)
        self.assertEqual(stats.errors, [])
