import json
import logging

from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _

from src.catalog.constants import PRODUCT_SLUG
from src.catalog.models import DomeModel
from src.catalog.views import get_dome_by_slug

from .models import ConfigOption
from .utils import (
    calculate_price,
    dome_base_price,
    format_diameter,
    preview_photos_for,
    tier_delta_for,
)

logger = logging.getLogger('src')


class ConfiguratorView(TemplateView):
    template_name = 'configurator/index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = _('Конфігуратор куполу — KUPOLLA')
        ctx['meta_description'] = _(
            'Налаштуйте комплектацію купола KUPOLLA: оберіть рівень оснащення та додаткові опції.'
        )

        product = get_dome_by_slug(self.request.GET.get('model'))
        ctx['product'] = product
        ctx['base_price'] = dome_base_price(product)
        ctx['product_slug'] = product.slug if product else PRODUCT_SLUG
        ctx['diameter_value'] = format_diameter(product)
        ctx['preview_photos'] = preview_photos_for(product)
        ctx['preview_photo_base'] = ctx['preview_photos']['base']
        ctx['catalog_models'] = DomeModel.objects.filter(
            is_published=True
        ).order_by('order', 'area_m2')
        ctx['selected_model'] = ctx['product_slug']

        tiers = list(ConfigOption.objects.filter(
            option_type=ConfigOption.OptionType.TIER, is_active=True
        ))
        for opt in tiers:
            opt.display_delta = tier_delta_for(
                product, opt.code, int(opt.price_delta or 0)
            )
        ctx['tier_options'] = tiers
        ctx['addon_options'] = ConfigOption.objects.filter(
            option_type=ConfigOption.OptionType.ADDON, is_active=True
        )
        return ctx


class CalculatorView(View):
    """POST /api/configurator/calculate/ — розраховує вартість конфігурації."""

    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except (json.JSONDecodeError, AttributeError):
            data = request.POST.dict()

        if not data.get('model'):
            data['model'] = PRODUCT_SLUG

        result = calculate_price(data)
        return JsonResponse(result)
