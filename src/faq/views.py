from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _

from .models import FAQGroup
from src.leads.models import Lead


class FaqView(TemplateView):
    template_name = 'faq/index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = _('FAQ — Часті запитання — KUPOLLA')
        ctx['meta_description'] = _('Відповіді на часті запитання про купольні будинки KUPOLLA: монтаж, ціна, дозволи, експлуатація.')
        ctx['groups'] = FAQGroup.objects.prefetch_related('items').all()
        from src.leads.forms import LeadForm
        ctx['faq_form'] = LeadForm(initial={'form_type': Lead.FormType.FAQ})
        return ctx
