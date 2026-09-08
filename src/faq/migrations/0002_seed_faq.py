from django.db import migrations

from src.faq.defaults import seed_faq


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            lambda apps, schema_editor: seed_faq(apps),
            migrations.RunPython.noop,
        ),
    ]
