"""Дефолтні дані для галереї KUPOLLA (сторінка 6 з «Правок»).

Два блоки на одній сторінці: «Купол» (екстерʼєр/інтерʼєр) і
«Виробництво» (проєкт, матеріали, конструктив). Кадрів із цеху
в медіа немає — у виробництво ставимо технічні та матеріальні фото.
"""

GALLERY_PHOTOS = (
    {
        'static_path': 'gallery/concept/concept-ext-forest-morning.webp',
        'title': 'Купол у лісі — ранковий туман',
        'alt': 'KUPOLLA — купольний будинок у лісі вранці',
        'category': 'dome',
        'project_type': 'glamping',
        'order': 10,
    },
    {
        'static_path': 'gallery/concept/concept-ext-resort-day.webp',
        'title': 'Курортний комплекс куполів',
        'alt': 'KUPOLLA — кілька купольних будинків на курорті',
        'category': 'dome',
        'project_type': 'commercial',
        'order': 20,
    },
    {
        'static_path': 'gallery/concept/concept-ext-mountain-lake.webp',
        'title': 'Купол біля гірського озера',
        'alt': 'KUPOLLA — купольний будинок на березі гірського озера',
        'category': 'dome',
        'project_type': 'glamping',
        'order': 30,
    },
    {
        'static_path': 'gallery/concept/concept-ext-autumn.webp',
        'title': 'Купол восени',
        'alt': 'KUPOLLA — купольний будинок в осінньому лісі',
        'category': 'dome',
        'project_type': 'living',
        'order': 40,
    },
    {
        'static_path': 'gallery/concept/concept-int-living-kitchen.webp',
        'title': 'Вітальня та кухня всередині купола',
        'alt': 'KUPOLLA — інтер\'єр вітальні та кухні',
        'category': 'dome',
        'project_type': 'living',
        'order': 50,
    },
    {
        'static_path': 'gallery/concept/concept-int-bathroom.webp',
        'title': 'Ванна кімната',
        'alt': 'KUPOLLA — інтер\'єр ванної кімнати',
        'category': 'dome',
        'project_type': 'living',
        'order': 60,
    },
    {
        'static_path': 'gallery/concept/concept-ext-waterfall.webp',
        'title': 'Купол біля водоспаду',
        'alt': 'KUPOLLA — купольний будинок біля водоспаду',
        'category': 'dome',
        'project_type': 'glamping',
        'order': 70,
    },
    {
        'static_path': 'gallery/concept/concept-ext-coast.webp',
        'title': 'Купол на побережжі',
        'alt': 'KUPOLLA — купольний будинок на морському побережжі',
        'category': 'dome',
        'project_type': 'commercial',
        'order': 80,
    },
    {
        'static_path': 'gallery/concept/concept-int-kitchen-counter.webp',
        'title': 'Кухонна зона',
        'alt': 'KUPOLLA — кухонна зона всередині купола',
        'category': 'dome',
        'project_type': 'living',
        'order': 90,
    },
    {
        'static_path': 'plans/concept-floorplan-top.webp',
        'title': 'Проєктування планування',
        'alt': 'KUPOLLA — план купола зверху',
        'category': 'production',
        'project_type': 'living',
        'order': 110,
    },
    {
        'static_path': 'materials/aisi316_connectors_card.webp',
        'title': 'Зʼєднувачі AISI 316',
        'alt': 'KUPOLLA — нержавіючі зʼєднувачі каркасу',
        'category': 'production',
        'project_type': 'living',
        'order': 120,
    },
    {
        'static_path': 'materials/triple_glass_card.webp',
        'title': 'Трошарове скло',
        'alt': 'KUPOLLA — ізолювальний склопакет',
        'category': 'production',
        'project_type': 'living',
        'order': 130,
    },
    {
        'static_path': 'gallery/concept/concept-int-wall-detail.webp',
        'title': 'CLT-панелі оболонки',
        'alt': 'KUPOLLA — геодезичні CLT-панелі внутрішньої оболонки',
        'category': 'production',
        'project_type': 'living',
        'order': 140,
    },
    {
        'static_path': 'materials/dome-shell-section.webp',
        'title': 'Конструктивний розріз',
        'alt': 'KUPOLLA — архітектурний розріз оболонки купола',
        'category': 'production',
        'project_type': 'living',
        'order': 150,
    },
)


def seed_gallery_photos():
    """Наповнює галерею блоками «Купол» і «Виробництво»."""
    from src.gallery.models import GalleryPhoto
    from src.core.seed_utils import assign_image_field

    for item in GALLERY_PHOTOS:
        photo, _created = GalleryPhoto.objects.get_or_create(
            order=item['order'],
            defaults={
                'title': item['title'],
                'title_uk': item['title'],
                'alt': item['alt'],
                'alt_uk': item['alt'],
                'category': item['category'],
                'project_type': item['project_type'],
            },
        )
        assign_image_field(photo, 'image', item['static_path'], 'gallery')
        photo.title = item['title']
        photo.title_uk = item['title']
        photo.alt = item['alt']
        photo.alt_uk = item['alt']
        photo.category = item['category']
        photo.project_type = item['project_type']
        photo.is_published = True
        photo.save()
