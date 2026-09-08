from django.db import migrations

from src.gallery.defaults import seed_gallery_photos


def forwards(apps, schema_editor):
    seed_gallery_photos()


class Migration(migrations.Migration):
    """Наповнює галерею стартовим набором фото купола (категорія dome)."""

    dependencies = [
        ('gallery', '0002_galleryphoto_category'),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
