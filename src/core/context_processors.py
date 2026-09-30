from django.conf import settings
from django.templatetags.static import static

from .i18n import enabled_language_codes, localize_path
from .models import SiteSettings


def site_settings(request):
    path = request.get_full_path()
    site = SiteSettings.load()
    public_codes = set(enabled_language_codes(site))
    switcher = []
    urls = {}
    for code, name in settings.LANGUAGES:
        if code not in public_codes:
            continue
        localized = localize_path(path, code)
        urls[code] = localized
        switcher.append({'code': code, 'name': str(name), 'url': localized})
    canonical = request.build_absolute_uri(request.path)
    host = f'{request.scheme}://{request.get_host()}'
    return {
        'site_settings': site,
        'lang_switch_urls': urls,
        'lang_switcher': switcher,
        'canonical_url': canonical,
        'hreflang_abs': {
            code: f'{host}{localized}' for code, localized in urls.items()
        },
        'og_image_url': request.build_absolute_uri(static('images/hero/kupolla-dome-forest.webp')),
    }
