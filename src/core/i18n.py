"""Prefix-swap для i18n URL. Українська без префікса, інші мови — /{код}/."""
from urllib.parse import urlsplit, urlunsplit

from django.conf import settings

_LANG_CODES = tuple(code for code, _name in settings.LANGUAGES)


def _split_path_query(path: str) -> tuple[str, str]:
    parts = urlsplit(path)
    path_only = parts.path or '/'
    query = urlunsplit(('', '', '', parts.query, parts.fragment))
    return path_only, query


def strip_language_prefix(path: str) -> str:
    path_only, query = _split_path_query(path)
    changed = True
    while changed:
        changed = False
        for code in _LANG_CODES:
            prefix = f'/{code}'
            if path_only == prefix or path_only == prefix + '/':
                path_only = '/'
                changed = True
                break
            if path_only.startswith(prefix + '/'):
                path_only = path_only[len(prefix):] or '/'
                changed = True
                break
    return path_only + query


def localize_path(path: str, lang: str) -> str:
    path_only, query = _split_path_query(strip_language_prefix(path))
    if not path_only.startswith('/'):
        path_only = '/' + path_only
    if lang == settings.LANGUAGE_CODE:
        return path_only + query
    localized = f'/{lang}/' if path_only == '/' else f'/{lang}{path_only}'
    return localized + query


def language_enabled(code: str, site_settings=None) -> bool:
    """Українська завжди відкрита. Інші мови — лише з тумблером у SiteSettings."""
    if code == settings.LANGUAGE_CODE:
        return True
    if site_settings is None:
        from src.core.models import SiteSettings
        site_settings = SiteSettings.load()
    return bool(getattr(site_settings, f'{code}_enabled', False))


def enabled_language_codes(site_settings=None) -> list[str]:
    if site_settings is None:
        from src.core.models import SiteSettings
        site_settings = SiteSettings.load()
    return [code for code, _name in settings.LANGUAGES if language_enabled(code, site_settings)]


def public_language_redirect(full_path: str, site_settings=None) -> tuple[str | None, bool]:
    """Повертає (ціль, permanent). None — редірект не потрібен."""
    collapsed = collapse_double_prefix(full_path)
    path_only, _query = _split_path_query(collapsed)
    segments = [part for part in path_only.split('/') if part]
    head = segments[0] if segments else ''
    if head == settings.LANGUAGE_CODE:
        return localize_path(collapsed, settings.LANGUAGE_CODE), True
    if head in _LANG_CODES and not language_enabled(head, site_settings):
        return localize_path(collapsed, settings.LANGUAGE_CODE), False
    if collapsed != full_path:
        return collapsed, False
    return None, False


def collapse_double_prefix(path: str) -> str:
    path_only, query = _split_path_query(path)
    had_slash = path_only.endswith('/') and path_only != '/'
    segments = [s for s in path_only.split('/') if s]
    while len(segments) >= 2 and segments[0] in _LANG_CODES and segments[1] in _LANG_CODES:
        segments.pop(0)
    if not segments:
        collapsed = '/'
    else:
        collapsed = '/' + '/'.join(segments)
        if had_slash:
            collapsed += '/'
    return collapsed + query
