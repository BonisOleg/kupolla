"""CRM webhook — джерело URL з SiteSettings або .env."""
import logging
import re
from urllib.parse import urlparse

from decouple import config

from .models import SiteSettings

logger = logging.getLogger('src')

# Приклади / демо-URL, які не слід викликати в продакшені
_PLACEHOLDER_PATH_FRAGMENTS = (
    '/kupolla/leads',
    '/your-webhook',
    '/example',
    '/changeme',
    '/placeholder',
)

_MAKE_HOOK_PATH_RE = re.compile(r'^/[a-zA-Z0-9_-]{8,}$')


def get_crm_webhook_url() -> str:
    site = SiteSettings.load()
    if site.crm_webhook_url:
        return site.crm_webhook_url.strip()
    return config('CRM_WEBHOOK_URL', default='').strip()


def is_configured_crm_webhook(url: str) -> bool:
    """Перевіряє, чи URL схожий на реальний webhook, а не на заглушку з .env.example."""
    url = (url or '').strip()
    if not url:
        return False

    parsed = urlparse(url)
    if parsed.scheme != 'https' or not parsed.netloc:
        logger.warning('CRM webhook має бути HTTPS URL: %s', url)
        return False

    path_lower = parsed.path.lower()
    for fragment in _PLACEHOLDER_PATH_FRAGMENTS:
        if fragment in path_lower:
            logger.warning('CRM webhook виглядає як заглушка, пропускаємо: %s', url)
            return False

    if 'make.com' in parsed.netloc and not _MAKE_HOOK_PATH_RE.match(parsed.path):
        logger.warning(
            'CRM webhook Make.com має містити унікальний токен у шляху, пропускаємо: %s',
            url,
        )
        return False

    return True


def build_lead_payload(lead) -> dict:
    """Формує JSON для Make.com / n8n / інших CRM."""
    dome = lead.dome_model
    config_data = lead.configurator_data
    if isinstance(config_data, str):
        try:
            import json
            config_data = json.loads(config_data)
        except (ValueError, TypeError):
            pass

    return {
        'id': lead.pk,
        'form_type': lead.form_type,
        'form_type_label': lead.get_form_type_display(),
        'name': lead.name,
        'phone': lead.phone,
        'email': lead.email or '',
        'country': lead.country or '',
        'city': lead.city or '',
        'message': lead.message or '',
        'dome_model_id': dome.pk if dome else None,
        'dome_model_slug': dome.slug if dome else None,
        'dome_model_name': dome.name if dome else None,
        'equipment_tier': lead.equipment_tier or '',
        'configurator_data': config_data,
        'ip_address': str(lead.ip_address) if lead.ip_address else None,
        'created_at': lead.created_at.isoformat() if lead.created_at else None,
    }
