from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _

from .models import AboutPage, TechnologiesPage


class AboutView(TemplateView):
    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = _('KUPOLLA - модульні будинки')
        ctx['meta_description'] = _('Виробник купольних будинків KUPOLLA: місія, команда, виробництво та шоурум.')
        ctx['about'] = AboutPage.load()
        ctx['team_members'] = ctx['about'].members.filter(is_published=True)
        return ctx


class TechnologiesView(TemplateView):
    template_name = 'pages/technologies.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = _('Матеріали — KUPOLLA')
        ctx['meta_description'] = _('Багатошарова оболонка купола, ACP-покриття, матеріали, енергоефективність та гарантії KUPOLLA.')
        ctx['tech'] = TechnologiesPage.load()
        return ctx
