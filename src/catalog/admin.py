from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin, TabularInline

from src.core.admin_utils import ImageSizeHelpMixin, TinyMCEAdminMixin, english_ready, image_size_notice
from src.core.image_specs import FLOOR_PLAN_IMAGE, MODEL_IMAGE

from .models import DomeModel, ModelImage, ModelSpec


class ModelImageInline(ImageSizeHelpMixin, TabularInline):
    model = ModelImage
    extra = 1
    fields = ('image', 'image_preview', 'alt', 'is_main', 'order')
    readonly_fields = ('image_preview',)
    image_size_help = {'image': MODEL_IMAGE}
    verbose_name = 'Фото'
    verbose_name_plural = 'Фото моделі'

    def image_preview(self, obj):
        if obj.image:
            from django.utils.html import format_html
            return format_html(
                '<img src="{}" alt="" style="height:60px;border-radius:4px;object-fit:cover;">',
                obj.image.url,
            )
        return '—'
    image_preview.short_description = 'Превʼю'


class ModelSpecInline(TabularInline):
    model = ModelSpec
    extra = 2
    fields = ('key', 'value', 'order')
    ordering = ('order',)
    verbose_name = 'Характеристика'
    verbose_name_plural = 'Характеристики (переклад — через поля _uk, _en у рядку)'


@admin.register(DomeModel)
class DomeModelAdmin(ImageSizeHelpMixin, TinyMCEAdminMixin, TabbedTranslationAdmin, ModelAdmin):
    tinymce_fields = ('description', 'floor_plan_note')
    image_size_help = {'floor_plan_image': FLOOR_PLAN_IMAGE}
    list_display = ('name', 'area_m2', 'purpose', 'size_cat', 'price_from', 'en_ready', 'is_published', 'is_featured', 'order')
    en_fields = ('name', 'short_description', 'description')
    list_editable = ('is_published', 'is_featured', 'order')
    list_filter = ('purpose', 'size_cat', 'is_published')
    list_filter_submit = True
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('floor_plan_preview',)
    inlines = [ModelImageInline, ModelSpecInline]

    fieldsets = (
        ('Основне', {
            'fields': ('name', 'slug', 'short_description', 'description'),
            'description': (
                'Короткий опис — plain text. Поле «Опис» — HTML через редактор (відображається на сторінці моделі).'
            ),
        }),
        ('Планування', {
            'fields': ('floor_plan_image', 'floor_plan_preview', 'floor_plan_note'),
            'description': image_size_notice(
                'Зображення плану:',
                FLOOR_PLAN_IMAGE,
            ),
        }),
        ('Параметри', {
            'fields': ('area_m2', 'diameter', 'height_m', 'insulation_mm', 'purpose', 'size_cat'),
        }),
        ('Ціни (€)', {
            'fields': ('price_base', 'price_standard', 'price_premium'),
            'description': 'Ціна «від» на сайті — мінімальна з трьох пакетів.',
        }),
        ('Публікація', {
            'fields': ('is_published', 'is_featured', 'order'),
            'description': '«На головній» — показувати в блоці featured на головній сторінці.',
        }),
    )

    @admin.display(boolean=True, description='EN')
    def en_ready(self, obj):
        return english_ready(obj, self.en_fields)

    def price_from(self, obj):
        return f'€{obj.price_from:,.0f}' if obj.price_from else '—'
    price_from.short_description = 'Ціна від'

    def floor_plan_preview(self, obj):
        if obj.floor_plan_image:
            from django.utils.html import format_html
            return format_html(
                '<img src="{}" alt="" style="max-height:120px;border-radius:4px;">',
                obj.floor_plan_image.url,
            )
        return '—'
    floor_plan_preview.short_description = 'Превʼю планування'


# ModelImage редагується через inline у DomeModel — окремий пункт меню не потрібен.
