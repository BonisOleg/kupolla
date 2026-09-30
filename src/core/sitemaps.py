from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from src.catalog.models import DomeModel
from src.blog.models import Post
from src.core.i18n import enabled_language_codes


class _PublicLanguagesMixin:
    def get_languages_for_item(self, item):
        return enabled_language_codes()


class StaticSitemap(_PublicLanguagesMixin, Sitemap):
    changefreq = 'weekly'
    priority = 0.8
    i18n = True

    def items(self):
        return [
            'core:home',
            'about:index',
            'configurator:index',
            'technologies:index',
            'gallery:index',
            'blog:list',
            'faq:index',
            'contacts:index',
        ]

    def location(self, item):
        return reverse(item)


class DomeModelSitemap(_PublicLanguagesMixin, Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    i18n = True

    def items(self):
        return DomeModel.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at


class BlogPostSitemap(_PublicLanguagesMixin, Sitemap):
    changefreq = 'monthly'
    priority = 0.6
    i18n = True

    def items(self):
        return Post.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at
