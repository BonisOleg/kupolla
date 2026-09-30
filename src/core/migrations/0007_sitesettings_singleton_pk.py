from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_sitesettings_google_drive_url'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='sitesettings',
            constraint=models.CheckConstraint(
                condition=models.Q(pk=1),
                name='core_sitesettings_singleton_pk',
            ),
        ),
    ]
