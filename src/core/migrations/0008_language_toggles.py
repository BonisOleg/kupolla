from django.db import migrations, models


def strip_default_language_prefix(apps, schema_editor):
    SiteSettings = apps.get_model('core', 'SiteSettings')
    for row in SiteSettings.objects.all():
        changed = False
        for field in ('privacy_policy_url', 'terms_url'):
            value = getattr(row, field) or ''
            if value.startswith('/uk/'):
                setattr(row, field, '/' + value[len('/uk/'):])
                changed = True
            elif value == '/uk':
                setattr(row, field, '/')
                changed = True
        if changed:
            row.save(update_fields=['privacy_policy_url', 'terms_url'])


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_sitesettings_singleton_pk'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='en_enabled',
            field=models.BooleanField(default=True, verbose_name='English на сайті'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='sk_enabled',
            field=models.BooleanField(default=False, verbose_name='Slovenčina на сайті'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='cs_enabled',
            field=models.BooleanField(default=False, verbose_name='Čeština на сайті'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='nl_enabled',
            field=models.BooleanField(default=False, verbose_name='Nederlands на сайті'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='ru_enabled',
            field=models.BooleanField(default=False, verbose_name='Русский на сайті'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='es_enabled',
            field=models.BooleanField(default=False, verbose_name='Español на сайті'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='fr_enabled',
            field=models.BooleanField(default=False, verbose_name='Français на сайті'),
        ),
        migrations.RunPython(strip_default_language_prefix, migrations.RunPython.noop),
    ]
