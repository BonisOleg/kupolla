from pathlib import Path
from decouple import config
from django.urls import reverse_lazy

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='',
    cast=lambda v: [s.strip() for s in v.split(',') if s.strip()],
)

INSTALLED_APPS = [
    # modeltranslation MUST be before django.contrib.admin
    'modeltranslation',

    # Unfold MUST be before django.contrib.admin
    'unfold',
    'unfold.contrib.filters',
    'unfold.contrib.forms',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',

    # Third-party
    'tinymce',
    'django_htmx',
    'csp',

    # Project apps
    'src.core',
    'src.catalog',
    'src.pages',
    'src.blog',
    'src.faq',
    'src.gallery',
    'src.leads',
    'src.configurator',
]

MODELTRANSLATION_TRANSLATION_FILES = (
    'src.catalog.translation',
    'src.blog.translation',
    'src.faq.translation',
    'src.gallery.translation',
    'src.configurator.translation',
    'src.pages.translation',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'src.core.middleware.CollapseLanguagePrefixMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
    'csp.middleware.CSPMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'src.core.context_processors.site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'uk'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [
    ('uk', 'Українська'),
    ('en', 'English'),
    ('sk', 'Slovenčina'),
    ('cs', 'Čeština'),
    ('nl', 'Nederlands'),
    ('ru', 'Русский'),
    ('es', 'Español'),
    ('fr', 'Français'),
]

LOCALE_PATHS = [BASE_DIR / 'locale']

MODELTRANSLATION_DEFAULT_LANGUAGE = 'uk'
MODELTRANSLATION_LANGUAGES = ('uk', 'en', 'sk', 'cs', 'nl', 'ru', 'es', 'fr')
MODELTRANSLATION_FALLBACK_LANGUAGES = ('uk',)

# Static & Media
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
    # Existing frontend assets (css/, js/ at project root)
    ('css', BASE_DIR / 'css'),
    ('js', BASE_DIR / 'js'),
]

MEDIA_URL = config('MEDIA_URL', default='/media/')
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# TinyMCE
TINYMCE_DEFAULT_CONFIG = {
    'height': 400,
    'menubar': False,
    'plugins': 'link lists image code',
    'toolbar': (
        'undo redo | formatselect | bold italic underline | '
        'alignleft aligncenter alignright | bullist numlist | '
        'link image | code'
    ),
    'content_style': 'body { font-family: Inter, sans-serif; font-size: 16px; }',
    'relative_urls': False,
    'remove_script_host': False,
}

# CSP (Content Security Policy) — django-csp 4.0 format
CONTENT_SECURITY_POLICY = {
    # Alpine.js (Unfold) потребує unsafe-eval — виключаємо лише /admin/
    'EXCLUDE_URL_PREFIXES': ('/admin/',),
    'DIRECTIVES': {
        'default-src': ("'self'",),
        'script-src': (
            "'self'",
            'https://www.googletagmanager.com',
            'https://www.google-analytics.com',
        ),
        'style-src': ("'self'", 'https://fonts.googleapis.com', "'unsafe-inline'"),
        'font-src': ("'self'", 'https://fonts.gstatic.com'),
        'img-src': (
            "'self'",
            'data:',
            'https://www.google-analytics.com',
            'https://*.tile.openstreetmap.org',
            'https://tile.openstreetmap.org',
        ),
        'connect-src': ("'self'", 'https://www.google-analytics.com', 'https://analytics.google.com'),
        'frame-src': (
            "'self'",
            'https://www.openstreetmap.org',
            'https://www.google.com',
            'https://maps.google.com',
        ),
    },
}

UNFOLD = {
    'SITE_TITLE': 'KUPOLLA',
    'SITE_HEADER': 'KUPOLLA — Адмінпанель',
    'SITE_SYMBOL': 'cottage',
    'DASHBOARD_CALLBACK': 'src.core.admin_dashboard.admin_dashboard_callback',
    'COLORS': {
        'primary': {
            '50': '240 253 244',
            '100': '220 252 231',
            '200': '187 247 208',
            '300': '134 239 172',
            '400': '74 222 128',
            '500': '34 197 94',
            '600': '22 163 74',
            '700': '21 128 61',
            '800': '22 101 52',
            '900': '20 83 45',
            '950': '5 46 22',
        },
    },
    'SIDEBAR': {
        'show_search': True,
        'command_search': True,
        'show_all_applications': False,
        'navigation': [
            {
                'title': 'Огляд',
                'separator': False,
                'items': [
                    {
                        'title': 'Головна',
                        'icon': 'dashboard',
                        'link': reverse_lazy('admin:index'),
                    },
                ],
            },
            {
                'title': 'Налаштування',
                'separator': True,
                'items': [
                    {
                        'title': 'Налаштування сайту',
                        'icon': 'settings',
                        'link': reverse_lazy('admin:core_sitesettings_changelist'),
                    },
                ],
            },
            {
                'title': 'Каталог',
                'separator': True,
                'items': [
                    {
                        'title': 'Моделі куполів',
                        'icon': 'home',
                        'link': reverse_lazy('admin:catalog_domemodel_changelist'),
                    },
                    {
                        'title': 'Конфігуратор',
                        'icon': 'tune',
                        'link': reverse_lazy('admin:configurator_configoption_changelist'),
                    },
                ],
            },
            {
                'title': 'Контент',
                'separator': True,
                'items': [
                    {
                        'title': 'Про компанію',
                        'icon': 'info',
                        'link': reverse_lazy('admin:pages_aboutpage_changelist'),
                    },
                    {
                        'title': 'Технології',
                        'icon': 'science',
                        'link': reverse_lazy('admin:pages_technologiespage_changelist'),
                    },
                    {
                        'title': 'Галерея',
                        'icon': 'photo_library',
                        'link': reverse_lazy('admin:gallery_galleryphoto_changelist'),
                    },
                    {
                        'title': 'Статті блогу',
                        'icon': 'article',
                        'link': reverse_lazy('admin:blog_post_changelist'),
                    },
                    {
                        'title': 'Категорії блогу',
                        'icon': 'folder',
                        'link': reverse_lazy('admin:blog_category_changelist'),
                    },
                    {
                        'title': 'Теги блогу',
                        'icon': 'label',
                        'link': reverse_lazy('admin:blog_tag_changelist'),
                    },
                    {
                        'title': 'FAQ',
                        'icon': 'help',
                        'link': reverse_lazy('admin:faq_faqgroup_changelist'),
                    },
                ],
            },
            {
                'title': 'CRM',
                'separator': True,
                'items': [
                    {
                        'title': 'Заявки',
                        'icon': 'inbox',
                        'link': reverse_lazy('admin:leads_lead_changelist'),
                    },
                ],
            },
        ],
    },
}

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {'handlers': ['console'], 'level': 'WARNING'},
    'loggers': {
        'src': {'handlers': ['console'], 'level': 'INFO', 'propagate': False},
        'django': {'handlers': ['console'], 'level': 'WARNING', 'propagate': False},
    },
}
