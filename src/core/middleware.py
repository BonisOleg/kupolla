from django.http import HttpResponseRedirect

from .i18n import collapse_double_prefix


class CollapseLanguagePrefixMiddleware:
    """Redirect /uk/en/... → /en/... after LocaleMiddleware."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        collapsed = collapse_double_prefix(request.get_full_path())
        if collapsed != request.get_full_path():
            return HttpResponseRedirect(collapsed)
        return self.get_response(request)
