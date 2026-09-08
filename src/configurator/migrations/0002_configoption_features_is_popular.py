from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configurator', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='configoption',
            name='features',
            field=models.JSONField(blank=True, default=list, verbose_name='Особливості'),
        ),
        migrations.AddField(
            model_name='configoption',
            name='is_popular',
            field=models.BooleanField(default=False, verbose_name='Популярна'),
        ),
    ]
