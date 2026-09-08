from django.db import migrations

from src.pages.defaults import seed_team_members


def forwards(apps, schema_editor):
    seed_team_members(apps)


class Migration(migrations.Migration):
    """Наповнює блок «Команда» на сторінці «Про компанію» 7 особами."""

    dependencies = [
        ('pages', '0002_teammember'),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
