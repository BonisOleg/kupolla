from django.db import migrations

from src.catalog.defaults import seed_dome_models


def forwards(apps, schema_editor):
    seed_dome_models(apps)
    # Фото для нових моделей (Compact/Grand) призначаємо тут-таки, у межах
    # catalog-міграцій, щоб не залежати від порядку виконання core.0004
    # (seed_content), який може виконатись раніше або пізніше цієї міграції.
    from src.catalog.defaults import seed_dome_images
    seed_dome_images()


class Migration(migrations.Migration):
    """Розширює модельний ряд до 3 продуктів: Compact / Prime / Grand."""

    dependencies = [
        ('catalog', '0006_alter_modelimage_options'),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
