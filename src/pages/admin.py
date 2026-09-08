from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin

from src.core.admin_utils import ImagePreviewMixin, ImageSizeHelpMixin, SingletonModelAdminMixin, TinyMCEAdminMixin, image_size_notice
from src.core.image_specs import TEAM_PHOTO_IMAGE

from .models import AboutPage, TeamMember, TechnologiesPage


@admin.register(AboutPage)
class AboutPageAdmin(SingletonModelAdminMixin, TinyMCEAdminMixin, TabbedTranslationAdmin, ModelAdmin):
    tinymce_fields = ('mission_body', 'values_body', 'team_body', 'cooperation_body')

    fieldsets = (
        ('Місія', {
            'fields': ('mission_title', 'mission_body'),
            'description': 'Головний блок сторінки «Про компанію».',
        }),
        ('Цінності', {'fields': ('values_body',)}),
        ('Команда', {'fields': ('team_body',)}),
        ('Етапи співпраці', {'fields': ('cooperation_body',)}),
        ('CTA', {'fields': ('cta_title',), 'description': 'Заклик до дії внизу сторінки.'}),
    )


@admin.register(TeamMember)
class TeamMemberAdmin(ImagePreviewMixin, ImageSizeHelpMixin, TabbedTranslationAdmin, ModelAdmin):
    image_size_help = {'photo': TEAM_PHOTO_IMAGE}
    preview_height = 60
    list_display = ('get_image_preview', 'name', 'position', 'is_published', 'order')
    list_editable = ('is_published', 'order')
    list_filter = ('is_published',)
    search_fields = ('name', 'position')
    readonly_fields = ('get_image_preview',)

    fieldsets = (
        ('Фото', {
            'fields': ('photo', 'get_image_preview'),
            'description': image_size_notice('Рекомендований розмір:', TEAM_PHOTO_IMAGE),
        }),
        ('Дані', {'fields': ('name', 'position')}),
        ('Публікація', {'fields': ('is_published', 'order')}),
    )


@admin.register(TechnologiesPage)
class TechnologiesPageAdmin(SingletonModelAdminMixin, TinyMCEAdminMixin, TabbedTranslationAdmin, ModelAdmin):
    tinymce_fields = (
        'intro_body',
        'construction_body',
        'materials_body',
        'energy_body',
        'production_body',
        'certificates_body',
    )

    fieldsets = (
        ('Вступ', {'fields': ('intro_body',)}),
        ('Конструктив', {'fields': ('construction_body',)}),
        ('Матеріали', {'fields': ('materials_body',)}),
        ('Енергоефективність', {'fields': ('energy_body',)}),
        ('Виробництво', {'fields': ('production_body',)}),
        ('Сертифікати', {'fields': ('certificates_body',)}),
    )
