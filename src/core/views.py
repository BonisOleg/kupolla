from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _

from src.catalog.views import get_product_dome


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = _('KUPOLLA — Купольні будинки нового покоління')
        ctx['meta_description'] = _(
            'Виробник купольних будинків KUPOLLA. '
            'Екологічні, енергоефективні, сучасні куполи для проживання, глемпінгу та комерції.'
        )
        ctx['product'] = get_product_dome()
        ctx['models'] = self._get_models()
        ctx['latest_posts'] = self._get_latest_posts()
        return ctx

    @staticmethod
    def _get_models():
        from src.catalog.models import DomeModel
        return (
            DomeModel.objects.filter(is_published=True)
            .prefetch_related('images')
            .order_by('order', 'area_m2')
        )

    @staticmethod
    def _get_latest_posts():
        from src.blog.models import Post
        return (
            Post.objects.filter(is_published=True)
            .select_related('category')
            .order_by('-published_at', '-created_at')[:4]
        )


class HealthCheckView(View):
    def get(self, request):
        return JsonResponse({'status': 'ok'})
