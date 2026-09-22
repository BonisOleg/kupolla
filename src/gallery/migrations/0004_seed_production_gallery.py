from django.db import migrations

from src.gallery.defaults import seed_gallery_photos


def forwards(apps, schema_editor):
    seed_gallery_photos()


class Migration(migrations.Migration):
    """Додає фото блоку «Виробництво» і оновлює наявні записи галереї."""

    dependencies = [
        ('gallery', '0003_seed_gallery_photos'),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
