from django.db import migrations


def forwards(apps, schema_editor):
    from src.blog.defaults import seed_blog
    from src.catalog.defaults import seed_dome_images
    from src.core.defaults import seed_site_settings
    from src.pages.defaults import seed_pages

    seed_dome_images()
    seed_blog()
    seed_pages()
    # Історична модель: у живій SiteSettings вже є поля з пізніших міграцій.
    seed_site_settings(apps)


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
