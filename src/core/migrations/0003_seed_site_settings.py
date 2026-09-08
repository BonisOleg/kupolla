from django.db import migrations

from src.core.defaults import seed_site_settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_sitesettings_map_embed_url_sitesettings_telegram_and_more'),
    ]

    operations = [
        migrations.RunPython(
            lambda apps, schema_editor: seed_site_settings(apps),
            migrations.RunPython.noop,
        ),
    ]
