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
        'price_base': 40000,
        'price_standard': 47000,
        'price_premium': 56000,
        'is_featured': False,
        'order': 1,
        'extra_specs': (('Монтаж', '5–7 днів'),),
    },
    {
        'slug': 'kupolla-s',
        'name': 'KUPOLLA Prime',
        'area_m2': 35,
        'diameter': '6.8',
        'height_m': '4.0',
        'purpose': 'glamping',
        'size_cat': 'medium',
        'short_description': 'Геодезичний купольний будинок для глемпінгу, відпочинку та гостьового проживання.',
        'description': (
            'KUPOLLA Prime — геодезичний купольний будинок площею 35 м². '
            'Найпопулярніша модель: компактна, енергоефективна і готова до життя в природі — '
            'ідеально для глемпінгу, романтичного відпочинку або гостьового будинку.'
        ),
        'price_base': 55000,
        'price_standard': 67000,
        'price_premium': 82000,
        'is_featured': True,
        'order': 2,
        'extra_specs': (('Монтаж', '7–10 днів'),),
    },
    {
        'slug': 'kupolla-grand',
        'name': 'KUPOLLA Grand',
        'area_m2': 80,
        'diameter': '9.5',
        'height_m': '4.8',
        'purpose': 'commercial',
        'size_cat': 'large',
        'short_description': 'Просторий купол для преміальних номерів, ресторану чи резиденції.',
        'description': (
            'KUPOLLA Grand — геодезичний купол площею 80 м² для проєктів, де важливі простір '
            'і статус: преміальний номер готелю, ресторан з панорамним видом або комфортна '
            'резиденція для постійного проживання.'
        ),
        'price_base': 130000,
        'price_standard': 146000,
        'price_premium': 167000,
        'is_featured': False,
        'order': 3,
        'extra_specs': (('Монтаж', '10–14 днів'),),
    },
)

MODEL_MAIN_IMAGE = {
    'kupolla-compact': (
        'models/kupolla-compact-lake.webp',
        'KUPOLLA Compact — купол біля озера',
    ),
    'kupolla-s': (
        'models/kupolla-s-exterior-forest.webp',
        'KUPOLLA Prime — купол у лісі',
    ),
    'kupolla-grand': (
        'models/kupolla-grand-resort.webp',
        'KUPOLLA Grand — курортний комплекс куполів',
    ),
}


_AREA_COPY_FIXES = (
    ('36 м²', '35 м²'),
    ('36 m²', '35 m²'),
    ('58 м²', '80 м²'),
    ('58 m²', '80 m²'),
)


def _sync_area_copy(dome):
    """Підтягує площі в перекладах опису після зміни моделі."""
    changed = False
    for field in dome._meta.fields:
        if field.name.startswith(('description', 'short_description', 'floor_plan_note')):
            val = getattr(dome, field.name, None)
            if not val:
                continue
            new = val
            for old, repl in _AREA_COPY_FIXES:
                new = new.replace(old, repl)
            if new != val:
                setattr(dome, field.name, new)
                changed = True
    if changed:
        dome.save()


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
        _sync_area_copy(dome)

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


def _gallery_main(slug):
    path, alt = MODEL_MAIN_IMAGE[slug]
    return {'static_path': path, 'alt': alt, 'is_main': True, 'order': 0}


DOME_GALLERIES = {
    'kupolla-compact': (
        _gallery_main('kupolla-compact'),
        {
            'static_path': 'models/kupolla-compact-night.webp',
            'alt': 'KUPOLLA Compact — вечірнє підсвічування біля стежки',
            'is_main': False,
            'order': 1,
        },
        {
            'static_path': 'models/kupolla-compact-firepit.webp',
            'alt': 'KUPOLLA Compact — тераса з вогнищем',
            'is_main': False,
            'order': 2,
        },
        {
            'static_path': 'models/kupolla-compact-interior.webp',
            'alt': 'KUPOLLA Compact — вітальня та кухня',
            'is_main': False,
            'order': 3,
        },
        {
            'static_path': 'models/kupolla-compact-bedroom.webp',
            'alt': 'KUPOLLA Compact — спальня',
            'is_main': False,
            'order': 4,
        },
    ),
    'kupolla-s': (
        _gallery_main('kupolla-s'),
        {
            'static_path': 'models/kupolla-s-night-terrace.webp',
            'alt': 'KUPOLLA Prime — вечірня тераса',
            'is_main': False,
            'order': 1,
        },
        {
            'static_path': 'models/kupolla-s-meadow.webp',
            'alt': 'KUPOLLA Prime — купол на галявині',
            'is_main': False,
            'order': 2,
        },
        {
            'static_path': 'models/kupolla-s-interior-lounge.webp',
            'alt': 'KUPOLLA Prime — панорамна вітальня',
            'is_main': False,
            'order': 3,
        },
        {
            'static_path': 'models/kupolla-s-interior-studio.webp',
            'alt': 'KUPOLLA Prime — спальня та кухня',
            'is_main': False,
            'order': 4,
        },
    ),
    'kupolla-grand': (
        _gallery_main('kupolla-grand'),
        {
            'static_path': 'models/kupolla-grand-aerial.webp',
            'alt': 'KUPOLLA Grand — курортний комплекс з висоти',
            'is_main': False,
            'order': 1,
        },
        {
            'static_path': 'models/kupolla-grand-pool.webp',
            'alt': 'KUPOLLA Grand — куполи біля басейну',
            'is_main': False,
            'order': 2,
        },
        {
            'static_path': 'models/kupolla-grand-interior-view.webp',
            'alt': 'KUPOLLA Grand — вітальня з панорамним видом',
            'is_main': False,
            'order': 3,
        },
        {
            'static_path': 'models/kupolla-grand-interior-suite.webp',
            'alt': 'KUPOLLA Grand — спальня люкс',
            'is_main': False,
            'order': 4,
        },
    ),
}

DOME_FLOOR_PLANS = {
    'kupolla-compact': {
        'static_path': 'plans/kupolla-compact-floor-plan.webp',
        'note': (
            'Планування 24 м²: спальня, міні-кухня та санвузол. '
            'Діаметр 5.5 м — для глемпінгу та швидкого запуску.'
        ),
    },
    'kupolla-s': {
        'static_path': 'plans/kupolla-s-floor-plan.webp',
        'note': (
            'Відкритий простір 35 м² з зоною відпочинку, спальнею та міні-кухнею. '
            'Панорамні вікна на 270° — максимум природного світла.'
        ),
    },
    'kupolla-grand': {
        'static_path': 'plans/kupolla-grand-elevation.webp',
        'note': (
            'Схема більшої моделі: відкритий простір 80 м² з панорамним фасадом '
            'для преміального номера, ресторану чи резиденції.'
        ),
    },
}

# Зворотна сумісність для старих імпортів / міграцій.
DOME_IMAGES = DOME_GALLERIES['kupolla-s']
FLOOR_PLAN_STATIC = DOME_FLOOR_PLANS['kupolla-s']['static_path']


def _set_floor_plan_note(dome, note):
    if not dome.floor_plan_note:
        dome.floor_plan_note = note
        if hasattr(dome, 'floor_plan_note_uk'):
            dome.floor_plan_note_uk = note
        return
    for field in ('floor_plan_note', 'floor_plan_note_uk', 'floor_plan_note_en'):
        val = getattr(dome, field, None)
        if val and '36 м²' in val:
            setattr(dome, field, val.replace('36 м²', '35 м²'))
        elif val and '36 m²' in val:
            setattr(dome, field, val.replace('36 m²', '35 m²'))


def seed_dome_images():
    """Копіює зображення з static/ у media/catalog/ для кожної моделі."""
    from src.catalog.models import DomeModel, ModelImage
    from src.core.seed_utils import assign_image_field

    for slug, items in DOME_GALLERIES.items():
        dome = DomeModel.objects.filter(slug=slug).first()
        if not dome:
            continue

        plan = DOME_FLOOR_PLANS.get(slug)
        if plan:
            assign_image_field(dome, 'floor_plan_image', plan['static_path'], 'catalog/plans')
            _set_floor_plan_note(dome, plan['note'])
            dome.save()

        kept_orders = []
        for item in items:
            img, _ = ModelImage.objects.get_or_create(
                dome=dome,
                order=item['order'],
                defaults={
                    'alt': item['alt'],
                    'is_main': item['is_main'],
                },
            )
            assign_image_field(img, 'image', item['static_path'], 'catalog')
            img.alt = item['alt']
            img.is_main = item['is_main']
            img.save()
            kept_orders.append(item['order'])

        ModelImage.objects.filter(dome=dome).exclude(order__in=kept_orders).delete()
