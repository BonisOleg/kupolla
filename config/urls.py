from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.contrib.sitemaps.views import sitemap
from django.views.generic import RedirectView, TemplateView

from src.core.views_i18n import set_language

from src.core.sitemaps import StaticSitemap, DomeModelSitemap, BlogPostSitemap

sitemaps = {
    'static': StaticSitemap,
    'models': DomeModelSitemap,
    'blog': BlogPostSitemap,
}

urlpatterns = [
    path(
        'favicon.ico',
        RedirectView.as_view(url=f'{settings.STATIC_URL}favicon.ico', permanent=True),
    ),
    path('admin/', admin.site.urls),
    path('healthz/', include('src.core.urls_health')),
    path('api/forms/', include('src.leads.urls')),
    path('api/configurator/', include('src.configurator.urls_api')),
    path('i18n/setlang/', set_language, name='set_language'),
    path('tinymce/', include('tinymce.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='core/robots.txt', content_type='text/plain')),
]

urlpatterns += i18n_patterns(
    path('', include('src.core.urls')),
    path('about/', include('src.pages.urls_about')),
    path('models/', include('src.catalog.urls')),
    path('configurator/', include('src.configurator.urls')),
    path('technologies/', include('src.pages.urls_technologies')),
    path('gallery/', include('src.gallery.urls')),
    path('blog/', include('src.blog.urls')),
    path('faq/', include('src.faq.urls')),
    path('contacts/', include('src.leads.urls_contacts')),
    prefix_default_language=True,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
