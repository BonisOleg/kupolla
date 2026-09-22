from django.db import migrations

from src.catalog.defaults import seed_dome_images, seed_dome_models


def forwards(apps, schema_editor):
    seed_dome_models(apps)
    seed_dome_images()


class Migration(migrations.Migration):
    """Compact 24 м² / 40k€, Prime 35 м² / 55k€, Grand 80 м² / 130k€."""

    dependencies = [
        ('catalog', '0007_three_dome_models'),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
