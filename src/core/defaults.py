"""Початкові налаштування сайту."""
from decouple import config

SITE_SETTINGS = {
    'company_name': 'KUPOLLA',
    'phone': '+38 067 173 75 78',
    'phone_eu': '+420 737 306 111',
    'email': 'office@kupolla.com',
    'working_hours': 'Пн–Пт: 9:00–18:00 (EET)',
    'address': 'Україна, Київ',
    'privacy_policy_url': '/uk/privacy/',
    'terms_url': '/uk/terms/',
    'telegram': 'https://t.me/kupolla',
    'instagram': 'https://instagram.com/kupolla',
}


def seed_site_settings(apps=None):
    if apps is not None:
        SiteSettings = apps.get_model('core', 'SiteSettings')
    else:
        from src.core.models import SiteSettings

    from src.core.crm import is_configured_crm_webhook

    valid_fields = {f.name for f in SiteSettings._meta.get_fields()}
    defaults = {k: v for k, v in SITE_SETTINGS.items() if k in valid_fields}
    crm_url = config('CRM_WEBHOOK_URL', default='').strip()
    if is_configured_crm_webhook(crm_url):
        defaults['crm_webhook_url'] = crm_url

    ga4 = config('GA4_MEASUREMENT_ID', default='').strip()
    if ga4:
        defaults['ga4_measurement_id'] = ga4

    SiteSettings.objects.update_or_create(pk=1, defaults=defaults)


def sync_site_settings_from_env():
    """Оновлює SiteSettings з .env (CRM, GA4) без перезапису інших полів."""
    from src.core.models import SiteSettings

    site = SiteSettings.load()
    changed = False

    from src.core.crm import is_configured_crm_webhook

    crm_url = config('CRM_WEBHOOK_URL', default='').strip()
    if is_configured_crm_webhook(crm_url) and site.crm_webhook_url != crm_url:
        site.crm_webhook_url = crm_url
        changed = True

    ga4 = config('GA4_MEASUREMENT_ID', default='').strip()
    if ga4 and site.ga4_measurement_id != ga4:
        site.ga4_measurement_id = ga4
        changed = True

    if changed:
        site.save()
