from django.db import migrations

from src.catalog.defaults import seed_dome_images


def forwards(apps, schema_editor):
    seed_dome_images()


class Migration(migrations.Migration):
    """Галерея та планування для Compact / Prime / Grand."""

    dependencies = [
        ('catalog', '0008_update_areas_prices'),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
