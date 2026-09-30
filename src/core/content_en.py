"""Англійські тексти CMS. Міграція заповнює порожні *_en, не чіпає вже введені."""

SPEC = {
    'Матеріал каркасу': 'Frame material',
    'CLT-панелі': 'CLT panels',
    'Вікна': 'Windows',
    '3-шарове, U=0.6': 'Triple glazing, U=0.6',
    'Фундамент': 'Foundation',
    'Гвинтові палі': 'Screw piles',
    'Клас енергоефективності': 'Energy class',
    'Гарантія на каркас': 'Frame warranty',
    '25 років': '25 years',
    'Снігове навантаження': 'Snow load',
    '500 кг/м²': '500 kg/m²',
    'Вітростійкість': 'Wind resistance',
    'до 200 км/год': 'up to 200 km/h',
    'Монтаж': 'Installation',
    '5–7 днів': '5–7 days',
    '7–10 днів': '7–10 days',
    '10–14 днів': '10–14 days',
    '14–18 днів': '14–18 days',
    '18–24 дні': '18–24 days',
}

DOMES = {
    'kupolla-compact': {
        'short_description': 'A compact dome for glamping and a fast launch of a hospitality site.',
        'description': (
            'KUPOLLA Compact is a 24 m² geodesic dome for a first glamping unit, '
            'a pilot location or a small guest house, with a modest starting investment.'
        ),
        'floor_plan_note': (
            '24 m² layout: bedroom, kitchenette and bathroom. '
            'A 5.5 m diameter for glamping and a fast launch.'
        ),
    },
    'kupolla-s': {
        'short_description': 'A geodesic dome house for glamping, leisure and guest stays.',
        'description': (
            'KUPOLLA Prime is a 35 m² geodesic dome house. The most popular model: '
            'compact, energy-efficient and ready for life outdoors — for glamping, '
            'a short stay or a guest house.'
        ),
        'floor_plan_note': (
            'An open 35 m² plan with a lounge, a bedroom and a kitchenette. '
            '270° panoramic glazing for maximum daylight.'
        ),
    },
    'kupolla-m': {
        'short_description': 'A practical dome house for family living.',
        'description': (
            'KUPOLLA M is a 64 m² model for family living, a short-stay rental '
            'or a small hospitality cluster.'
        ),
    },
    'kupolla-grand': {
        'short_description': 'A spacious dome for a premium room, a restaurant or a residence.',
        'description': (
            'KUPOLLA Grand is an 80 m² geodesic dome for projects where space matters: '
            'a premium hotel room, a restaurant with a panoramic view, or a residence.'
        ),
        'floor_plan_note': (
            'An 80 m² open plan with a panoramic facade for a premium room, '
            'a restaurant or a residence.'
        ),
    },
    'kupolla-l': {
        'short_description': 'A spacious dome house for year-round living.',
        'description': (
            'KUPOLLA L is a 120 m² dome house for a family home or a premium hotel suite.'
        ),
    },
    'kupolla-xl': {
        'short_description': 'A premium model for a residence or a commercial project.',
        'description': (
            'KUPOLLA XL is a 200 m² premium dome house. Maximum volume and a free plan '
            'for a residence or a commercial building.'
        ),
    },
}

FAQ_GROUPS = {
    'Монтаж та виробництво': 'Installation and production',
    'Ціноутворення та оплата': 'Pricing and payment',
    'Дозволи та документи': 'Permits and documents',
    'Експлуатація та обслуговування': 'Use and maintenance',
}

FAQ_ITEMS = {
    'Скільки часу займає монтаж купольного будинку?': (
        'How long does it take to install a dome house?',
        '<p>The frame takes 3 to 7 working days depending on the model. '
        'The full cycle, including insulation, windows and the outer shell, takes 10–14 days.</p>',
    ),
    'Які умови потрібні для монтажу? Чи потрібен фундамент?': (
        'What does installation require? Is a foundation needed?',
        '<p>On most soils we use screw piles: fast, with no excavation, and suitable for uneven ground. '
        'For year-round living we recommend a strip or slab foundation. '
        'Our engineers confirm the choice after a look at the site geology.</p>',
    ),
    'Чи можна встановити купол на схилі або нерівній ділянці?': (
        'Can a dome be built on a slope or uneven ground?',
        '<p>Yes. Screw piles can take a slope of up to 15°. For steeper sites we design the pile lengths individually, '
        'so the natural ground can stay in place.</p>',
    ),
    'Хто проводить монтаж? Чи можу я зробити це самостійно?': (
        'Who installs the dome? Can I do it myself?',
        '<p>A certified KUPOLLA crew installs the dome. We do not recommend self-build: '
        'assembly quality affects durability and the warranty. Crews travel across Europe.</p>',
    ),
    'Що включає ціна «від...»?': (
        'What does the “from” price include?',
        '<p>The base price includes the CLT frame, 200 mm insulation, the outer shell, '
        'standard windows and doors, and frame assembly. It does not include the foundation, '
        'interior finishes, delivery, utilities or a terrace unless that option is selected.</p>',
    ),
    'Як здійснюється оплата? Чи є розстрочка?': (
        'How do you pay? Is instalment available?',
        '<p>The usual schedule is 30% when the contract is signed, 50% before shipment and 20% after installation. '
        'We also work with partner banks on a loan or lease.</p>',
    ),
    'Чи змінюється ціна після укладення договору?': (
        'Does the price change after the contract is signed?',
        '<p>The contract price is fixed at signing. Any later change of configuration is a written addendum '
        'with its own fixed cost.</p>',
    ),
    'Чи потрібен дозвіл на будівництво для купола?': (
        'Does a dome need a building permit?',
        '<p>It depends on the country, the floor area and how the building is classified. '
        'Temporary structures under 50 m² in much of the EU need no permit, or only a notification. '
        'A permanent home follows the normal permit process. We supply the project documents for the application.</p>',
    ),
    'Яку документацію ви надаєте?': (
        'What documents do you provide?',
        '<p>We provide the architectural design, structural calculations, material specifications, '
        'CE certificates, a building passport and a maintenance guide. '
        'On request we prepare the package for a building permit.</p>',
    ),
    'Як часто потрібне технічне обслуговування?': (
        'How often is maintenance needed?',
        '<p>We recommend a yearly inspection for the first five years, then every three years. '
        'The main checks are joint tightness, the shell and the connectors. '
        'A service contract with a site visit is available.</p>',
    ),
    'Чи придатний купол для проживання взимку?': (
        'Is the dome suitable for winter living?',
        '<p>Yes. 200 mm of insulation and energy class A+ keep the interior comfortable down to −30°C. '
        'The dome suits a Nordic or Alpine climate. Heating use is about 30% lower than in a conventional house.</p>',
    ),
    'Чи можна розширити або змінити купол після встановлення?': (
        'Can the dome be extended or altered after installation?',
        '<p>You can add a terrace or link two domes with a tunnel. Interior partitions can change freely: '
        'only the outer frame is structural. We advise on what is possible.</p>',
    ),
    'Що відбувається після закінчення терміну служби?': (
        'What happens at the end of the service life?',
        '<p>CLT timber and the steel connectors can be recycled. With maintenance the structure lasts 50+ years. '
        'The dome can also be dismantled and moved.</p>',
    ),
}

CATEGORIES = {
    'Глемпінг': 'Glamping',
    'Дизайн': 'Design',
    'Екологія': 'Ecology',
    'Технології': 'Technology',
}

CONFIG = {
    'terrace': 'Terrace 6 m²',
    'panoramic': 'Panoramic windows',
    'solar': 'Solar panels',
    'smarthome': 'Smart Home',
    'kupolla-s': 'KUPOLLA Prime 35 m²',
    'base': 'Base',
    'standard': 'Standard',
    'premium': 'Premium',
}

GALLERY = {
    'KUPOLLA — Панорамний фасад': ('KUPOLLA — Panoramic facade', 'KUPOLLA geodesic dome, front view'),
    'KUPOLLA — Лісовий глемпінг': ('KUPOLLA — Forest glamping', 'KUPOLLA dome in a pine forest'),
    'KUPOLLA — Осінній краєвид': ('KUPOLLA — Autumn view', 'KUPOLLA dome by a lake in autumn'),
    'KUPOLLA — Тераса з видом': ('KUPOLLA — Terrace with a view', 'KUPOLLA glamping dome with a timber terrace'),
    'KUPOLLA — Природне середовище': ('KUPOLLA — Natural setting', 'KUPOLLA geodesic dome outdoors'),
    'KUPOLLA — Берег озера': ('KUPOLLA — Lake shore', 'KUPOLLA dome on a rock by a lake'),
    'Купол у лісі — ранковий туман': ('Dome in the forest — morning mist', 'KUPOLLA dome house in a forest at morning'),
    'Курортний комплекс куполів': ('A resort cluster of domes', 'Several KUPOLLA dome houses at a resort'),
    'Купол біля гірського озера': ('Dome by a mountain lake', 'KUPOLLA dome house on a mountain lake shore'),
    'Купол восени': ('Dome in autumn', 'KUPOLLA dome house in an autumn forest'),
    'Вітальня та кухня всередині купола': ('Living room and kitchen inside the dome', 'KUPOLLA living room and kitchen interior'),
    'Ванна кімната': ('Bathroom', 'KUPOLLA bathroom interior'),
    'Купол біля водоспаду': ('Dome by a waterfall', 'KUPOLLA dome house beside a waterfall'),
    'Купол на побережжі': ('Dome on the coast', 'KUPOLLA dome house on the seashore'),
    'Кухонна зона': ('Kitchen zone', 'KUPOLLA kitchen inside the dome'),
    'Проєктування планування': ('Floor-plan design', 'KUPOLLA dome plan from above'),
    'Зʼєднувачі AISI 316': ('AISI 316 connectors', 'KUPOLLA stainless frame connectors'),
    'Трошарове скло': ('Triple glazing', 'KUPOLLA insulating glass unit'),
    'CLT-панелі оболонки': ('CLT shell panels', 'KUPOLLA geodesic CLT panels of the inner shell'),
    'Конструктивний розріз': ('Construction section', 'KUPOLLA architectural section of the dome shell'),
}

ABOUT = {
    'mission_title': 'Who we are',
    'mission_body': (
        '<p>KUPOLLA designs modular dome buildings for hotels, resorts and investment projects.</p>'
        '<p>We develop dome architecture that meets the practical demands of commercial use. '
        'An aluminium-composite outer shell gives the building durable performance and a clear architectural form.</p>'
        '<div class="kp-about-story__nums">'
        '<div><strong>50+</strong> completed projects</div>'
        '<div><strong>8</strong> countries</div>'
        '<div><strong>96 mo.</strong> warranty</div>'
        '<div><strong>A+</strong> energy class</div>'
        '</div>'
    ),
    'values_body': (
        '<ul>'
        '<li><strong>Ecology</strong> — natural materials, a low carbon footprint, and a light touch on the site.</li>'
        '<li><strong>Innovation</strong> — from CLT structures to Smart Home systems in a dome.</li>'
        '<li><strong>Quality</strong> — checks at every stage, from raw material to handover.</li>'
        '<li><strong>Clarity</strong> — open pricing, fixed dates, full documentation and support.</li>'
        '</ul>'
    ),
    'cooperation_body': (
        '<ol>'
        '<li><strong>Consultation</strong> — we discuss the brief, the budget and the site.</li>'
        '<li><strong>Design</strong> — we prepare the project and the estimate.</li>'
        '<li><strong>Production</strong> — we manufacture the dome elements at the factory.</li>'
        '<li><strong>Delivery</strong> — we ship the kit to the site.</li>'
        '<li><strong>Installation</strong> — our crew assembles the dome in 7–14 days.</li>'
        '<li><strong>Support</strong> — we stay with you through the warranty period.</li>'
        '</ol>'
    ),
    'team_body': (
        '<p>The KUPOLLA team is structural engineers, architects, production technologists and installers '
        'with dome projects in 8 European countries.</p>'
    ),
    'cta_title': 'Ready to start?',
}

TECH = {
    'intro_body': (
        '<p>A geodesic dome is one of the most stable structures in nature. '
        'KUPOLLA combines that form with current materials and factory production '
        'to build energy-class A+ housing.</p>'
    ),
    'construction_body': (
        '<p>A geodesic sphere is the most efficient closed form: the least surface for the most volume.</p>'
        '<ul>'
        '<li>About 30% less heat loss than a rectangular building of the same floor area</li>'
        '<li>Load shared across every member of the structure</li>'
        '<li>Snow load of 500 kg/m² and wind up to 200 km/h</li>'
        '<li>Even acoustics and natural air movement inside</li>'
        '</ul>'
    ),
    'materials_body': (
        '<h3>CLT panels</h3>'
        '<p>Cross-laminated timber from PEFC/FSC forests. Strong for its weight, renewable and CO₂-neutral.</p>'
        '<h3>Triple glazing</h3>'
        '<p>An insulating unit, U=0.6 W/m²K, argon-filled, with a low-E coating.</p>'
        '<h3>AISI 316 connectors</h3>'
        '<p>Marine-grade stainless steel. Resistant to corrosion, moisture and UV.</p>'
    ),
    'energy_body': (
        '<p>KUPOLLA insulation is specified for −30°C to +40°C.</p>'
        '<ul>'
        '<li>200 mm mineral wool, λ=0.035 W/mK</li>'
        '<li>A continuous vapour barrier without thermal bridges</li>'
        '<li>Heat recovery at 85% efficiency</li>'
        '<li>Option: solar panels and a ground-source heat pump</li>'
        '</ul>'
        '<p><strong>Class A+</strong> · heat loss about 30% lower · U=0.6 for the glass</p>'
    ),
    'production_body': (
        '<ol>'
        '<li><strong>Design and documents</strong> (1–2 weeks) — 3D model, structural drawings, specifications.</li>'
        '<li><strong>CLT production</strong> (2–3 weeks) — accuracy to 0.5 mm, numbered parts.</li>'
        '<li><strong>Foundation</strong> (2–5 days) — screw piles or a concrete slab.</li>'
        '<li><strong>Frame assembly</strong> (3–5 days) — a crew of four.</li>'
        '<li><strong>Insulation and roof</strong> (2–3 days) — every joint sealed.</li>'
        '<li><strong>Windows and doors</strong> (1–2 days).</li>'
        '</ol>'
    ),
    'certificates_body': (
        '<ul>'
        '<li><strong>CE marking</strong> — compliance with EU construction rules</li>'
        '<li><strong>FSC / PEFC</strong> — certified forestry</li>'
        '<li><strong>Class A+</strong> — the top energy class</li>'
        '<li><strong>25-year warranty</strong> — on the load-bearing frame</li>'
        '<li><strong>Independent testing</strong> — laboratory tests of the materials</li>'
        '</ul>'
    ),
}


def _fill(obj, field, value):
    if not value:
        return False
    current = getattr(obj, f'{field}_en', None) or ''
    if str(current).strip():
        return False
    setattr(obj, f'{field}_en', value)
    return True


def apply_english(apps, schema_editor):
    DomeModel = apps.get_model('catalog', 'DomeModel')
    ModelSpec = apps.get_model('catalog', 'ModelSpec')
    for dome in DomeModel.objects.all():
        payload = DOMES.get(dome.slug, {})
        changed = False
        for field, value in payload.items():
            changed = _fill(dome, field, value) or changed
        if changed:
            dome.save()
    for spec in ModelSpec.objects.all():
        changed = _fill(spec, 'key', SPEC.get(spec.key_uk or '', ''))
        changed = _fill(spec, 'value', SPEC.get(spec.value_uk or '', '')) or changed
        if changed:
            spec.save()

    FAQGroup = apps.get_model('faq', 'FAQGroup')
    FAQItem = apps.get_model('faq', 'FAQItem')
    for group in FAQGroup.objects.all():
        if _fill(group, 'name', FAQ_GROUPS.get(group.name_uk or '', '')):
            group.save()
    for item in FAQItem.objects.all():
        pair = FAQ_ITEMS.get(item.question_uk or '')
        if not pair:
            continue
        changed = _fill(item, 'question', pair[0])
        changed = _fill(item, 'answer', pair[1]) or changed
        if changed:
            item.save()

    Category = apps.get_model('blog', 'Category')
    for category in Category.objects.all():
        if _fill(category, 'name', CATEGORIES.get(category.name_uk or '', '')):
            category.save()

    from src.core.content_en_posts import POSTS
    Post = apps.get_model('blog', 'Post')
    for post in Post.objects.all():
        payload = POSTS.get(post.slug, {})
        changed = False
        for field, value in payload.items():
            changed = _fill(post, field, value) or changed
        if changed:
            post.save()

    AboutPage = apps.get_model('pages', 'AboutPage')
    TechnologiesPage = apps.get_model('pages', 'TechnologiesPage')
    about = AboutPage.objects.filter(pk=1).first()
    if about:
        changed = False
        for field, value in ABOUT.items():
            changed = _fill(about, field, value) or changed
        if changed:
            about.save()
    tech = TechnologiesPage.objects.filter(pk=1).first()
    if tech:
        changed = False
        for field, value in TECH.items():
            changed = _fill(tech, field, value) or changed
        if changed:
            tech.save()

    TeamMember = apps.get_model('pages', 'TeamMember')
    for member in TeamMember.objects.all():
        if _fill(member, 'position', member.position_uk or member.position or ''):
            member.save()

    ConfigOption = apps.get_model('configurator', 'ConfigOption')
    for option in ConfigOption.objects.all():
        if _fill(option, 'name', CONFIG.get(option.code, '')):
            option.save()

    GalleryPhoto = apps.get_model('gallery', 'GalleryPhoto')
    for photo in GalleryPhoto.objects.all():
        pair = GALLERY.get(photo.title_uk or '')
        if not pair:
            continue
        changed = _fill(photo, 'title', pair[0])
        changed = _fill(photo, 'alt', pair[1]) or changed
        if changed:
            photo.save()
