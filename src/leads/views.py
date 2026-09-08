import logging

from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _

from .forms import ContactForm, HeroForm, LeadForm
from .models import Lead

logger = logging.getLogger('src')


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


class LeadCreateView(TemplateView):
    """Приймає заявки з усіх форм сайту (HTMX POST)."""

    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        if (request.POST.get('website') or '').strip():
            logger.info('Lead honeypot triggered from %s', get_client_ip(request))
            if request.htmx:
                return self._htmx_success(request, None)
            return JsonResponse({'status': 'ok'})

        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)
            lead.ip_address = get_client_ip(request)
            lead.save()
            logger.info('New lead created: #%s %s (%s)', lead.pk, lead.name, lead.form_type)

            if request.htmx:
                return self._htmx_success(request, lead)
            return JsonResponse({'status': 'ok', 'id': lead.pk})

        logger.warning('Lead form invalid: %s', form.errors)
        if request.htmx:
            return self._htmx_error(request, form)
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

    def _htmx_success(self, request, lead):
        from django.template.loader import render_to_string
        html = render_to_string('leads/partials/form_success.html', {'lead': lead}, request=request)
        response = HttpResponse(html)
        response['HX-Trigger'] = 'formSuccess'
        return response

    def _htmx_error(self, request, form):
        from django.template.loader import render_to_string
        html = render_to_string('leads/partials/form_errors.html', {'form': form}, request=request)
        return HttpResponse(html, status=422)


class ContactsView(TemplateView):
    template_name = 'leads/contacts.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = _('Контакти — KUPOLLA')
        ctx['meta_description'] = _('Контакти KUPOLLA: адреса, телефон, email, форма зворотного зв\'язку.')
        ctx['form'] = ContactForm(initial={'form_type': Lead.FormType.CONTACT})
        return ctx
