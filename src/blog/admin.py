from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin

from src.core.admin_utils import ImageSizeHelpMixin, TinyMCEAdminMixin, english_ready, image_size_notice
from src.core.image_specs import BLOG_COVER_IMAGE

from .models import Category, Tag, Post


@admin.register(Category)
class CategoryAdmin(TabbedTranslationAdmin, ModelAdmin):
    list_display = ('name', 'slug', 'post_count')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = 'Статей'


@admin.register(Tag)
class TagAdmin(TabbedTranslationAdmin, ModelAdmin):
    list_display = ('name', 'slug', 'post_count')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = 'Статей'


@admin.register(Post)
class PostAdmin(ImageSizeHelpMixin, TinyMCEAdminMixin, TabbedTranslationAdmin, ModelAdmin):
    tinymce_fields = ('body',)
    image_size_help = {'cover_image': BLOG_COVER_IMAGE}
    list_display = ('title', 'category', 'en_ready', 'is_published', 'published_at', 'cover_preview')
    en_fields = ('title', 'excerpt', 'body')
    list_filter = ('is_published', 'category', 'tags')
    list_filter_submit = True
    search_fields = ('title', 'excerpt', 'body')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    date_hierarchy = 'published_at'
    readonly_fields = ('cover_preview',)

    fieldsets = (
        ('Контент', {
            'fields': ('title', 'slug', 'excerpt', 'body', 'cover_image', 'cover_preview'),
            'description': image_size_notice('Обкладинка статті:', BLOG_COVER_IMAGE),
        }),
        ('Класифікація', {
            'fields': ('category', 'tags'),
        }),
        ('SEO', {
            'fields': ('seo_title', 'seo_description'),
            'classes': ('collapse',),
            'description': 'Якщо порожньо — використовуються заголовок і анонс статті.',
        }),
        ('Публікація', {
            'fields': ('is_published', 'published_at'),
            'description': 'Дата публікації впливає на сортування в списку статей.',
        }),
    )

    @admin.display(boolean=True, description='EN')
    def en_ready(self, obj):
        return english_ready(obj, self.en_fields)

    def cover_preview(self, obj):
        if obj.cover_image:
            from django.utils.html import format_html
            return format_html(
                '<img src="{}" alt="" style="max-height:120px;border-radius:4px;object-fit:cover;">',
                obj.cover_image.url,
            )
        return '—'
    cover_preview.short_description = 'Поточна обкладинка'
