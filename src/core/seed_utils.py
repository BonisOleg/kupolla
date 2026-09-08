"""Допоміжні функції для копіювання статичних зображень у media."""
from pathlib import Path

from django.conf import settings


def resolve_static_image(relative_path: str) -> Path | None:
    """Шукає файл у static/images/ або staticfiles/images/."""
    for base in (settings.BASE_DIR / 'static' / 'images', settings.BASE_DIR / 'staticfiles' / 'images'):
        candidate = base / relative_path
        if candidate.is_file():
            return candidate
    return None


def copy_static_image_to_media(relative_path: str, media_subdir: str) -> str | None:
    """
    Копіює static/images/<relative_path> → media/<media_subdir>/<filename>.
    Повертає шлях відносно MEDIA_ROOT для ImageField.
    """
    src = resolve_static_image(relative_path)
    if src is None:
        return None

    dest_dir = Path(settings.MEDIA_ROOT) / media_subdir
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_file = dest_dir / src.name

    if not dest_file.exists() or dest_file.stat().st_size != src.stat().st_size:
        dest_file.write_bytes(src.read_bytes())

    return f'{media_subdir}/{src.name}'


def assign_image_field(instance, field_name: str, relative_path: str, media_subdir: str) -> bool:
    """
    Призначає ImageField зі статичного файлу. Повертає True при успіху.

    Файл фізично копіюємо самі (copy_static_image_to_media) і одразу
    прив'язуємо готовий шлях до поля — без повторного field.save() /
    storage.save(), який би (побачивши, що файл із такою назвою вже є на
    диску) створив ЩЕ ОДНУ копію з випадковим суфіксом (_XXXXXXX). Це і
    спричиняло накопичення дублікатів у media/ при кожному повторному сидингу.
    """
    media_path = copy_static_image_to_media(relative_path, media_subdir)
    if not media_path:
        return False

    field = getattr(instance, field_name)
    field.name = media_path
    return True
