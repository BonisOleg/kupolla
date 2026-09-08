"""Початкові дані модельного ряду KUPOLLA: Compact / Prime / Grand."""

TRANSLATED_FIELDS = ('name', 'description', 'short_description')

COMMON_SPECS = (
    ('Матеріал каркасу', 'CLT-панелі'),
    ('Вікна', '3-шарове, U=0.6'),
    ('Фундамент', 'Гвинтові палі'),
    ('Клас енергоефективності', 'A+'),
    ('Гарантія на каркас', '25 років'),
    ('Снігове навантаження', '500 кг/м²'),
    ('Вітростійкість', 'до 200 км/год'),
)

DOME_MODELS = (
    {
        'slug': 'kupolla-compact',
        'name': 'KUPOLLA Compact',
        'area_m2': 24,
        'diameter': '5.5',
        'height_m': '3.6',
        'purpose': 'glamping',
        'size_cat': 'small',
        'short_description': 'Компактний купол для глемпінгу та швидкого запуску туристичного об\'єкта.',
        'description': (
            'KUPOLLA Compact — геодезичний купол площею 24 м² для тих, хто хочете почати '
            'з мінімальних інвестицій. Ідеально для першого юніта глемпінгу, тестового '
            'запуску локації або гостьового будинку невеликої площі.'
        ),
        'price_base': 22000,
        'price_standard': 29000,
        'price_premium': 38000,
        'is_featured': False,
        'order': 1,
        'extra_specs': (('Монтаж', '5–7 днів'),),
    },
    {
        'slug': 'kupolla-s',
        'name': 'KUPOLLA Prime',
        'area_m2': 36,
        'diameter': '6.8',
        'height_m': '4.0',
        'purpose': 'glamping',
        'size_cat': 'medium',
        'short_description': 'Геодезичний купольний будинок для глемпінгу, відпочинку та гостьового проживання.',
        'description': (
            'KUPOLLA Prime — геодезичний купольний будинок площею 36 м². '
            'Найпопулярніша модель: компактна, енергоефективна і готова до життя в природі — '
            'ідеально для глемпінгу, романтичного відпочинку або гостьового будинку.'
        ),
        'price_base': 35000,
        'price_standard': 47000,
        'price_premium': 62000,
        'is_featured': True,
        'order': 2,
        'extra_specs': (('Монтаж', '7–10 днів'),),
    },
    {
        'slug': 'kupolla-grand',
        'name': 'KUPOLLA Grand',
        'area_m2': 58,
        'diameter': '9.5',
        'height_m': '4.8',
        'purpose': 'commercial',
        'size_cat': 'large',
        'short_description': 'Просторий купол для преміальних номерів, ресторану чи резиденції.',
        'description': (
            'KUPOLLA Grand — геодезичний купол площею 58 м² для проєктів, де важливі простір '
            'і статус: преміальний номер готелю, ресторан з панорамним видом або комфортна '
            'резиденція для постійного проживання.'
        ),
        'price_base': 58000,
        'price_standard': 74000,
        'price_premium': 95000,
        'is_featured': False,
        'order': 3,
        'extra_specs': (('Монтаж', '10–14 днів'),),
    },
)

MODEL_MAIN_IMAGE = {
    'kupolla-compact': (
        'gallery/concept/concept-ext-forest-morning.webp',
        'KUPOLLA Compact — компактний купол у лісі',
    ),
    'kupolla-grand': (
        'gallery/concept/concept-ext-resort-day.webp',
        'KUPOLLA Grand — просторий купол для преміального відпочинку',
    ),
}


def _with_uk_fields(data):
    payload = dict(data)
    for field in TRANSLATED_FIELDS:
        if field in payload:
            payload[f'{field}_uk'] = payload[field]
    return payload


def seed_dome_models(apps):
    DomeModel = apps.get_model('catalog', 'DomeModel')
    ModelSpec = apps.get_model('catalog', 'ModelSpec')

    for item in DOME_MODELS:
        data = dict(item)
        extra_specs = data.pop('extra_specs', ())
        dome, _created = DomeModel.objects.update_or_create(
            slug=data['slug'],
            defaults=_with_uk_fields({
                **data,
                'insulation_mm': 200,
                'is_published': True,
            }),
        )

        ModelSpec.objects.filter(dome=dome).delete()
        order = 0
        for key, value in (*COMMON_SPECS, *extra_specs):
            ModelSpec.objects.create(
                dome=dome,
                key=key,
                key_uk=key,
                value=value,
                value_uk=value,
                order=order,
            )
            order += 1

    DomeModel.objects.filter(
        slug__in=('kupolla-m', 'kupolla-l', 'kupolla-xl'),
    ).update(is_published=False)


DOME_IMAGES = (
    {
        'static_path': 'models/kupolla-s-exterior-forest.webp',
        'alt': 'KUPOLLA — зовнішній вигляд у лісі',
        'is_main': True,
        'order': 0,
    },
    {
        'static_path': 'gallery/glamping-forest-kupolla-s.webp',
        'alt': 'KUPOLLA — глемпінг у лісовому оточенні',
        'is_main': False,
        'order': 1,
    },
    {
        'static_path': 'hero/kupolla-dome-forest.webp',
        'alt': 'KUPOLLA — купольний будинок у лісі',
        'is_main': False,
        'order': 2,
    },
    {
        'static_path': 'dome-geodesic-forest.webp',
        'alt': 'Геодезичний купол KUPOLLA',
        'is_main': False,
        'order': 3,
    },
)

FLOOR_PLAN_STATIC = 'plans/kupolla-s-floor-plan.webp'


def seed_dome_images():
    """Копіює зображення з static/ у media/catalog/ для KUPOLLA."""
    from src.catalog.models import DomeModel, ModelImage
    from src.core.seed_utils import assign_image_field

    dome = DomeModel.objects.filter(slug='kupolla-s').first()
    if not dome:
        return

    if not dome.floor_plan_image:
        assign_image_field(dome, 'floor_plan_image', FLOOR_PLAN_STATIC, 'catalog/plans')

    if not dome.floor_plan_note:
        dome.floor_plan_note = (
            'Відкритий простір 36 м² з зоною відпочинку, спальнею та міні-кухнею. '
            'Панорамні вікна на 270° — максимум природного світла.'
        )
        dome.floor_plan_note_uk = dome.floor_plan_note

    dome.save()

    for item in DOME_IMAGES:
        img, _ = ModelImage.objects.get_or_create(
            dome=dome,
            order=item['order'],
            defaults={
                'alt': item['alt'],
                'is_main': item['is_main'],
            },
        )
        if not img.image:
            assign_image_field(img, 'image', item['static_path'], 'catalog')
            img.alt = item['alt']
            img.is_main = item['is_main']
            img.save()

    for slug, (static_path, alt) in MODEL_MAIN_IMAGE.items():
        other = DomeModel.objects.filter(slug=slug).first()
        if not other:
            continue
        img, _created = ModelImage.objects.get_or_create(
            dome=other,
            order=0,
            defaults={'alt': alt, 'is_main': True},
        )
        if not img.image:
            assign_image_field(img, 'image', static_path, 'catalog')
            img.alt = alt
            img.is_main = True
            img.save()
