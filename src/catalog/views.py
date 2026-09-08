from django.http import HttpResponsePermanentRedirect
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.utils.translation import gettext_lazy as _

from .constants import DEPRECATED_SLUGS, PRODUCT_SLUG
from .models import DomeModel


def get_product_dome():
    """Повертає флагманську (featured) модель, з фолбеком на першу опубліковану."""
    published = DomeModel.objects.filter(is_published=True)
    return (
        published.filter(is_featured=True).order_by('order', 'pk').first()
        or published.order_by('order', 'pk').first()
    )


class ModelListView(ListView):
    """Модельний ряд KUPOLLA: Compact / Prime / Grand — з фільтрами."""

    model = DomeModel
    template_name = 'catalog/list.html'
    context_object_name = 'models'

    def get_queryset(self):
        return (
            DomeModel.objects.filter(is_published=True)
            .prefetch_related('images')
            .order_by('order', 'area_m2')
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = _('Модельний ряд купольних будинків — KUPOLLA')
        ctx['meta_description'] = _(
            'Compact, Prime або Grand — оберіть купольний будинок KUPOLLA під ваш проєкт та бюджет.'
        )
        ctx['purpose_choices'] = DomeModel.Purpose.choices
        ctx['size_choices'] = DomeModel.SizeCategory.choices
        ctx['area_ranges'] = [
            ('compact', _('до 50 м²')),
            ('standard', _('50–100 м²')),
            ('spacious', _('100+ м²')),
        ]
        ctx['price_ranges'] = [
            ('entry', _('до €50 000')),
            ('mid', _('€50 000–120 000')),
            ('top', _('від €120 000')),
        ]
        return ctx


class ModelDetailView(DetailView):
    model = DomeModel
    template_name = 'catalog/detail.html'
    context_object_name = 'dome'

    def dispatch(self, request, *args, **kwargs):
        slug = kwargs.get('slug', '')
        if slug in DEPRECATED_SLUGS:
            return HttpResponsePermanentRedirect(
                reverse('catalog:detail', kwargs={'slug': PRODUCT_SLUG})
            )
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return DomeModel.objects.filter(is_published=True).prefetch_related('images', 'specs')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        dome = self.get_object()
        ctx['page_title'] = dome.name
        ctx['meta_description'] = dome.short_description or dome.description[:160]
        return ctx
