from django.conf import settings
from django.templatetags.static import static

from .i18n import localize_path
from .models import SiteSettings


def site_settings(request):
    path = request.get_full_path()
    switcher = []
    urls = {}
    for code, name in settings.LANGUAGES:
        localized = localize_path(path, code)
        urls[code] = localized
        switcher.append({'code': code, 'name': str(name), 'url': localized})
    canonical = request.build_absolute_uri(request.path)
    host = f'{request.scheme}://{request.get_host()}'
    return {
        'site_settings': SiteSettings.load(),
        'lang_switch_urls': urls,
        'lang_switcher': switcher,
        'canonical_url': canonical,
        'hreflang_abs': {
            code: f'{host}{localize_path(path, code)}' for code, _ in settings.LANGUAGES
        },
        'og_image_url': request.build_absolute_uri(static('images/hero/kupolla-dome-forest.webp')),
    }
