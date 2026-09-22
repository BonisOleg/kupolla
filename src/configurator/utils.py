"""Логіка розрахунку ціни конфігуратора."""
import logging
from decimal import Decimal

from django.templatetags.static import static

from src.catalog.constants import PRODUCT_SLUG
from src.catalog.defaults import DOME_GALLERIES, MODEL_MAIN_IMAGE
from src.catalog.views import get_dome_by_slug

from .models import ConfigOption

logger = logging.getLogger('src')


def _get_option(option_type, code, alt_codes=()):
    codes = (code, *alt_codes)
    for lookup_code in codes:
        if not lookup_code:
            continue
        try:
            return ConfigOption.objects.get(
                code=lookup_code,
                option_type=option_type,
                is_active=True,
            )
        except ConfigOption.DoesNotExist:
            continue
    return None


def _as_list(value):
    if value is None:
        return []
    if isinstance(value, str):
        return [item.strip() for item in value.split(',') if item.strip()]
    if isinstance(value, (list, tuple, set)):
        return list(value)
    return []


def resolve_dome(raw_slug):
    return get_dome_by_slug(raw_slug)


def dome_base_price(dome):
    if dome and dome.price_base:
        return int(dome.price_base)
    return 55000


def tier_delta_for(dome, code, fallback=0):
    if not dome:
        return fallback
    base = dome.price_base or 0
    if code == 'base':
        return 0
    if code == 'standard' and dome.price_standard:
        return max(int(dome.price_standard - base), 0)
    if code == 'premium' and dome.price_premium:
        return max(int(dome.price_premium - base), 0)
    return fallback


def format_diameter(dome):
    if not dome or not dome.diameter:
        return '6.8m'
    value = str(dome.diameter).strip()
    return value if value.endswith('m') else f'{value}m'


def preview_photos_for(dome):
    slug = dome.slug if dome else PRODUCT_SLUG
    gallery = list(DOME_GALLERIES.get(slug, ()))
    paths = [item['static_path'] for item in gallery]
    if not paths:
        main = MODEL_MAIN_IMAGE.get(slug)
        paths = [main[0]] if main else ['models/kupolla-s-exterior-forest.webp']

    def url_at(index):
        path = paths[min(index, len(paths) - 1)]
        return static(f'images/{path}')

    premium_idx = 3 if len(paths) > 3 else (2 if len(paths) > 2 else 0)
    return {
        'base': url_at(0),
        'standard': url_at(1 if len(paths) > 1 else 0),
        'premium': url_at(premium_idx),
    }


def calculate_price(config: dict) -> dict:
    """
    config = {
        'model': 'kupolla-s',
        'diameter': '6.8m',
        'tier': 'standard',
        'addons': ['windows', 'terrace'],
    }
    Повертає: {'total': Decimal, 'breakdown': [...]}
    """
    total = Decimal('0')
    breakdown = []
    errors = []

    model_code = config.get('model') or PRODUCT_SLUG
    tier_code = config.get('tier')
    addon_codes = _as_list(config.get('addons'))
    dome = resolve_dome(model_code)

    if dome and dome.price_base:
        total += Decimal(dome.price_base)
        breakdown.append({'label': dome.name, 'price': float(dome.price_base)})
    else:
        model_opt = _get_option(ConfigOption.OptionType.MODEL, model_code)
        if model_opt:
            total += model_opt.base_price
            breakdown.append({'label': model_opt.name, 'price': float(model_opt.base_price)})
        else:
            errors.append(f'Невідома модель: {model_code}')
            logger.warning('Unknown model code: %s', model_code)

    if tier_code:
        tier_opt = _get_option(ConfigOption.OptionType.TIER, tier_code, (f'tier-{tier_code}',))
        fallback = int(tier_opt.price_delta) if tier_opt and tier_opt.price_delta else 0
        delta = Decimal(tier_delta_for(dome, tier_code, fallback))
        if delta:
            label = tier_opt.name if tier_opt else str(tier_code)
            breakdown.append({'label': label, 'price': float(delta)})
        total += delta

    for addon_code in addon_codes:
        addon_opt = _get_option(ConfigOption.OptionType.ADDON, addon_code)
        if addon_opt:
            total += addon_opt.price_delta
            breakdown.append({'label': addon_opt.name, 'price': float(addon_opt.price_delta)})
        else:
            logger.warning('Unknown addon code: %s', addon_code)

    return {
        'total': float(total),
        'breakdown': breakdown,
        'errors': errors,
    }
