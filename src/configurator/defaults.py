"""Початкові опції конфігуратора KUPOLLA."""

CONFIG_OPTIONS = (
    {
        'option_type': 'model',
        'code': 'kupolla-s',
        'name': 'KUPOLLA Prime 35 м²',
        'base_price': 55000,
        'price_delta': 0,
        'order': 1,
    },
    {
        'option_type': 'tier',
        'code': 'base',
        'name': 'Базова',
        'price_delta': 0,
        'features': ['CLT каркас', 'Стандартні вікна', 'Монтаж'],
        'order': 1,
    },
    {
        'option_type': 'tier',
        'code': 'standard',
        'name': 'Стандарт',
        'price_delta': 12000,
        'is_popular': True,
        'features': ['Панорамні вікна', 'Тераса 6 м²', 'Система опалення'],
        'order': 2,
    },
    {
        'option_type': 'tier',
        'code': 'premium',
        'name': 'Преміум',
        'price_delta': 27000,
        'features': ['Підлогове опалення', 'Smart Home', 'Преміум фінішинг'],
        'order': 3,
    },
    {
        'option_type': 'addon',
        'code': 'terrace',
        'name': 'Тераса 6 м²',
        'price_delta': 8500,
        'order': 1,
    },
    {
        'option_type': 'addon',
        'code': 'panoramic',
        'name': 'Панорамні вікна',
        'price_delta': 12000,
        'order': 2,
    },
    {
        'option_type': 'addon',
        'code': 'solar',
        'name': 'Сонячні панелі',
        'price_delta': 9000,
        'order': 3,
    },
    {
        'option_type': 'addon',
        'code': 'smarthome',
        'name': 'Smart Home',
        'price_delta': 6500,
        'order': 4,
    },
)


def seed_config_options(apps):
    ConfigOption = apps.get_model('configurator', 'ConfigOption')

    for item in CONFIG_OPTIONS:
        data = dict(item)
        features = data.pop('features', [])
        is_popular = data.pop('is_popular', False)
        name = data['name']
        ConfigOption.objects.update_or_create(
            code=data['code'],
            defaults={
                **data,
                'name_uk': name,
                'features': features,
                'is_popular': is_popular,
                'is_active': True,
            },
        )
