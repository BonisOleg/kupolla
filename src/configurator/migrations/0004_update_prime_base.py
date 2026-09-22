from django.db import migrations

from src.configurator.defaults import seed_config_options


def forwards(apps, schema_editor):
    seed_config_options(apps)


class Migration(migrations.Migration):
    """Базова ціна конфігуратора = Prime від 55 000 € / 35 м²."""

    dependencies = [
        ('configurator', '0003_seed_config_options'),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
