from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin, StackedInline

from src.core.admin_utils import TinyMCEAdminMixin

from .models import FAQGroup, FAQItem


class FAQItemInline(StackedInline):
    model = FAQItem
    extra = 1
    fields = ('question', 'answer', 'order', 'is_published')
    ordering = ('order',)
    show_change_link = True
    classes = ('collapse',)
    verbose_name = 'Питання'
    verbose_name_plural = (
        'Питання FAQ (відповідь — HTML; для зручного редагування натисніть «Змінити» → окрема форма з редактором)'
    )


@admin.register(FAQGroup)
class FAQGroupAdmin(TabbedTranslationAdmin, ModelAdmin):
    list_display = ('name', 'item_count', 'order')
    list_editable = ('order',)
    search_fields = ('name',)
    inlines = [FAQItemInline]

    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Питань'


@admin.register(FAQItem)
class FAQItemAdmin(TinyMCEAdminMixin, TabbedTranslationAdmin, ModelAdmin):
    tinymce_fields = ('answer',)
    list_display = ('question', 'group', 'is_published', 'order')
    list_editable = ('is_published', 'order')
    list_filter = ('group', 'is_published')
    list_filter_submit = True
    search_fields = ('question', 'answer')
    autocomplete_fields = ('group',)

    fieldsets = (
        ('Питання', {
            'fields': ('group', 'question', 'answer'),
            'description': 'Відповідь підтримує HTML — використовуйте редактор для списків і посилань.',
        }),
        ('Публікація', {
            'fields': ('order', 'is_published'),
        }),
    )
