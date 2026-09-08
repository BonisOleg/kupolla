from urllib.parse import unquote, urlparse

from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import check_for_language
from django.views.decorators.http import require_POST

from .i18n import collapse_double_prefix, localize_path


def _extract_next(request) -> str:
    raw = request.POST.get('next') or request.GET.get('next') or ''
    if not raw and request.META.get('HTTP_REFERER'):
        parsed = urlparse(request.META['HTTP_REFERER'])
        raw = parsed.path
        if parsed.query:
            raw = f'{raw}?{parsed.query}'
    raw = unquote(raw).strip()
    if not raw.startswith('/'):
        return '/'
    if not url_has_allowed_host_and_scheme(raw, allowed_hosts={request.get_host()}):
        return '/'
    return raw


@require_POST
def set_language(request):
    lang = request.POST.get('language', '')
    if not check_for_language(lang):
        lang = settings.LANGUAGE_CODE
    target = collapse_double_prefix(localize_path(_extract_next(request), lang))
    response = HttpResponseRedirect(target)
    response.set_cookie(
        settings.LANGUAGE_COOKIE_NAME,
        lang,
        max_age=getattr(settings, 'LANGUAGE_COOKIE_AGE', None),
        path=getattr(settings, 'LANGUAGE_COOKIE_PATH', '/'),
        domain=getattr(settings, 'LANGUAGE_COOKIE_DOMAIN', None),
        secure=getattr(settings, 'LANGUAGE_COOKIE_SECURE', False),
        httponly=getattr(settings, 'LANGUAGE_COOKIE_HTTPONLY', False),
        samesite=getattr(settings, 'LANGUAGE_COOKIE_SAMESITE', 'Lax'),
    )
    return response
