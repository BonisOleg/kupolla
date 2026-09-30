import django.db.models.deletion
from django.db import migrations, models


def attach_team_to_about(apps, schema_editor):
    AboutPage = apps.get_model('pages', 'AboutPage')
    TeamMember = apps.get_model('pages', 'TeamMember')
    page, _ = AboutPage.objects.get_or_create(pk=1)
    TeamMember.objects.filter(page__isnull=True).update(page_id=page.pk)


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_seed_team_members'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='aboutpage',
            constraint=models.CheckConstraint(
                condition=models.Q(pk=1),
                name='pages_aboutpage_singleton_pk',
            ),
        ),
        migrations.AddConstraint(
            model_name='technologiespage',
            constraint=models.CheckConstraint(
                condition=models.Q(pk=1),
                name='pages_technologiespage_singleton_pk',
            ),
        ),
        migrations.AddField(
            model_name='teammember',
            name='page',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='members',
                to='pages.aboutpage',
                verbose_name='Сторінка',
            ),
        ),
        migrations.RunPython(attach_team_to_about, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='teammember',
            name='page',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='members',
                to='pages.aboutpage',
                verbose_name='Сторінка',
            ),
        ),
    ]
