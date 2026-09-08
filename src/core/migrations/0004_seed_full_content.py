from django.db import migrations


def forwards(apps, schema_editor):
    from django.core.management import call_command
    call_command('seed_content', verbosity=0)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_seed_site_settings'),
        # 0005 додає поля до SiteSettings ДО того, як seed_content (нижче)
        # звертається до "живої" моделі SiteSettings — інакше на чистій БД
        # ORM намагається читати ще не створену колонку.
        ('core', '0005_sitesettings_phone_eu_alter_sitesettings_phone'),
        ('blog', '0001_initial'),
        ('pages', '0001_initial'),
        ('catalog', '0005_single_dome_product'),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
