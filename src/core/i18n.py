"""Prefix-swap для i18n URL. prefix_default_language=True — усі мови з префіксом."""
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
    localized = f'/{lang}/' if path_only == '/' else f'/{lang}{path_only}'
    return localized + query


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
