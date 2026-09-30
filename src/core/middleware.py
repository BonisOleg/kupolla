from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect

from .i18n import public_language_redirect

_SKIP_PREFIXES = (
    '/admin',
    '/static/',
    '/media/',
    '/api/',
    '/i18n/',
    '/tinymce/',
    '/healthz',
    '/favicon.ico',
    '/sitemap.xml',
    '/robots.txt',
)


class CollapseLanguagePrefixMiddleware:
    """/uk/… → без префікса (301); подвійний префікс і вимкнена мова → українська."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        if path.startswith(_SKIP_PREFIXES):
            return self.get_response(request)
        target, permanent = public_language_redirect(request.get_full_path())
        if target:
            redirect_cls = HttpResponsePermanentRedirect if permanent else HttpResponseRedirect
            return redirect_cls(target)
        return self.get_response(request)
