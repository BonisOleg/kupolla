from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin, TranslationStackedInline
from unfold.admin import ModelAdmin, StackedInline
from unfold.overrides import FORMFIELD_OVERRIDES_INLINE

from src.core.admin_utils import ImagePreviewMixin, ImageSizeHelpMixin, SingletonModelAdminMixin, TinyMCEAdminMixin
from src.core.image_specs import TEAM_PHOTO_IMAGE

from .models import AboutPage, TeamMember, TechnologiesPage


class TeamMemberInline(ImagePreviewMixin, ImageSizeHelpMixin, TranslationStackedInline, StackedInline):
    model = TeamMember
    formfield_overrides = FORMFIELD_OVERRIDES_INLINE
    extra = 0
    image_field = 'photo'
    preview_height = 72
    image_size_help = {'photo': TEAM_PHOTO_IMAGE}
    fields = ('photo', 'get_image_preview', 'name', 'position', 'is_published', 'order')
    readonly_fields = ('get_image_preview',)
    ordering = ('order', 'pk')
    verbose_name = 'Член команди'
    verbose_name_plural = 'Команда на сторінці «Про компанію»'


@admin.register(AboutPage)
class AboutPageAdmin(SingletonModelAdminMixin, TinyMCEAdminMixin, TabbedTranslationAdmin, ModelAdmin):
    tinymce_fields = ('mission_body', 'values_body', 'team_body', 'cooperation_body')
    inlines = [TeamMemberInline]

    fieldsets = (
        ('Місія', {
            'fields': ('mission_title', 'mission_body'),
            'description': 'Головний блок сторінки «Про компанію».',
        }),
        ('Цінності', {'fields': ('values_body',)}),
        ('Команда', {
            'fields': ('team_body',),
            'description': 'Текст секції. Картки людей — одразу під цією формою.',
        }),
        ('Етапи співпраці', {'fields': ('cooperation_body',)}),
        ('CTA', {'fields': ('cta_title',), 'description': 'Заклик до дії внизу сторінки.'}),
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
