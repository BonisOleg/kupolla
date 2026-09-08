import tempfile

from .base import *  # noqa: F401, F403

SECRET_KEY = 'test-only-insecure-key'

DEBUG = False

# Тести (через seed-міграції) копіюють файли у MEDIA_ROOT — використовуємо
# тимчасову директорію ОС, щоб не засмічувати робочий media/ дублікатами
# на кожен прогін `manage.py test`.
MEDIA_ROOT = tempfile.mkdtemp(prefix='kupolla_test_media_')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
