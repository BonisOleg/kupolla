from django.db import migrations

from src.catalog.defaults import DOME_MODELS, seed_dome_models


def forwards(apps, schema_editor):
    seed_dome_models(apps)


def backwards(apps, schema_editor):
    DomeModel = apps.get_model('catalog', 'DomeModel')
    slugs = [item['slug'] for item in DOME_MODELS]
    DomeModel.objects.filter(slug__in=slugs).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_domemodel_floor_plan_image_domemodel_floor_plan_note_and_more'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
