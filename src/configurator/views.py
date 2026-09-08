import json
import logging

from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _

from src.catalog.constants import PRODUCT_SLUG
from src.catalog.views import get_product_dome

from .models import ConfigOption
from .utils import calculate_price

logger = logging.getLogger('src')


class ConfiguratorView(TemplateView):
    template_name = 'configurator/index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = _('Конфігуратор куполу — KUPOLLA')
        ctx['meta_description'] = _(
            'Налаштуйте комплектацію купола KUPOLLA: оберіть рівень оснащення та додаткові опції.'
        )

        product = get_product_dome()
        ctx['product'] = product
        ctx['base_price'] = product.price_base if product and product.price_base else 35000
        ctx['product_slug'] = product.slug if product else PRODUCT_SLUG

        ctx['tier_options'] = ConfigOption.objects.filter(
            option_type=ConfigOption.OptionType.TIER, is_active=True
        )
        ctx['addon_options'] = ConfigOption.objects.filter(
            option_type=ConfigOption.OptionType.ADDON, is_active=True
        )

        ctx['selected_model'] = self.request.GET.get('model', ctx['product_slug'])
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
            data['model'] = 'kupolla-s'

        result = calculate_price(data)
        return JsonResponse(result)
