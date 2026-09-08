from django.db import migrations

from src.catalog.defaults import seed_dome_models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_seed_dome_models'),
    ]

    operations = [
        migrations.RunPython(
            lambda apps, schema_editor: seed_dome_models(apps),
            migrations.RunPython.noop,
        ),
    ]
