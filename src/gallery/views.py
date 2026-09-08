from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _

from .models import GalleryPhoto


class GalleryView(TemplateView):
    template_name = 'gallery/index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = _('Галерея реалізованих проєктів — KUPOLLA')
        ctx['meta_description'] = _('Фотогалерея купольних будинків KUPOLLA у природному оточенні.')
        published = GalleryPhoto.objects.filter(is_published=True)
        ctx['dome_photos'] = published.filter(category=GalleryPhoto.Category.DOME)
        ctx['production_photos'] = published.filter(category=GalleryPhoto.Category.PRODUCTION)
        return ctx
