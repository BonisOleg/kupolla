from django.db import migrations

from src.core.content_en import apply_english


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_language_toggles'),
        ('catalog', '0009_seed_model_galleries'),
        ('faq', '0002_seed_faq'),
        ('blog', '0001_initial'),
        ('pages', '0004_singleton_pk_and_team_page'),
        ('gallery', '0004_seed_production_gallery'),
        ('configurator', '0004_update_prime_base'),
    ]

    operations = [
        migrations.RunPython(apply_english, migrations.RunPython.noop),
    ]
