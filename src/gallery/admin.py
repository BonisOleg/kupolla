from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin

from src.core.admin_utils import ImagePreviewMixin, ImageSizeHelpMixin, english_ready, image_size_notice
from src.core.image_specs import GALLERY_IMAGE

from .models import GalleryPhoto


@admin.register(GalleryPhoto)
class GalleryPhotoAdmin(ImagePreviewMixin, ImageSizeHelpMixin, TabbedTranslationAdmin, ModelAdmin):
    image_size_help = {'image': GALLERY_IMAGE}
    preview_height = 120
    list_display = ('get_image_preview', 'title', 'category', 'project_type', 'en_ready', 'is_published', 'order')
    en_fields = ('title', 'alt')
    list_editable = ('is_published', 'order')
    list_filter = ('category', 'project_type', 'is_published')
    list_filter_submit = True
    search_fields = ('title', 'alt')
    readonly_fields = ('get_image_preview',)

    @admin.display(boolean=True, description='EN')
    def en_ready(self, obj):
        return english_ready(obj, self.en_fields)

    fieldsets = (
        ('Фото', {
            'fields': ('image', 'get_image_preview'),
            'description': image_size_notice('Рекомендований розмір:', GALLERY_IMAGE),
        }),
        ('Підпис', {
            'fields': ('title', 'alt'),
            'description': 'Alt — для SEO та доступності (опишіть, що на фото).',
        }),
        ('Публікація', {
            'fields': ('category', 'project_type', 'is_published', 'order'),
        }),
    )
