"""Логіка розрахунку ціни конфігуратора."""
import logging
from decimal import Decimal

from .models import ConfigOption

from src.catalog.constants import PRODUCT_SLUG

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


def calculate_price(config: dict) -> dict:
    """
    config = {
        'model': 'kupolla-m',
        'diameter': '7',
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
    addon_codes = config.get('addons', [])

    model_opt = _get_option(ConfigOption.OptionType.MODEL, model_code)
    if model_opt:
        total += model_opt.base_price
        breakdown.append({'label': model_opt.name, 'price': float(model_opt.base_price)})
    else:
        errors.append(f'Невідома модель: {model_code}')
        logger.warning('Unknown model code: %s', model_code)

    if tier_code:
        tier_opt = _get_option(ConfigOption.OptionType.TIER, tier_code, (f'tier-{tier_code}',))
        if tier_opt:
            total += tier_opt.price_delta
            if tier_opt.price_delta:
                breakdown.append({'label': tier_opt.name, 'price': float(tier_opt.price_delta)})
        else:
            logger.warning('Unknown tier code: %s', tier_code)

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
