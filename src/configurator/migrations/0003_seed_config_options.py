from django.db import migrations

from src.configurator.defaults import seed_config_options


class Migration(migrations.Migration):

    dependencies = [
        ('configurator', '0002_configoption_features_is_popular'),
    ]

    operations = [
        migrations.RunPython(
            lambda apps, schema_editor: seed_config_options(apps),
            migrations.RunPython.noop,
        ),
    ]
