from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin, TranslationStackedInline
from unfold.admin import ModelAdmin, StackedInline
from unfold.overrides import FORMFIELD_OVERRIDES_INLINE

from src.core.admin_utils import TinyMCEAdminMixin, english_ready

from .models import FAQGroup, FAQItem


class FAQItemInline(TinyMCEAdminMixin, TranslationStackedInline, StackedInline):
    model = FAQItem
    formfield_overrides = FORMFIELD_OVERRIDES_INLINE
    tinymce_fields = ('answer',)
    extra = 0
    fields = ('question', 'answer', 'order', 'is_published')
    ordering = ('order',)
    verbose_name = 'Питання'
    verbose_name_plural = 'Питання цієї групи'


@admin.register(FAQGroup)
class FAQGroupAdmin(TabbedTranslationAdmin, ModelAdmin):
    list_display = ('name', 'item_count', 'en_ready', 'order')
    list_editable = ('order',)
    search_fields = ('name',)
    inlines = [FAQItemInline]

    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Питань'

    @admin.display(boolean=True, description='EN')
    def en_ready(self, obj):
        items = list(obj.items.all())
        if not items:
            return False
        return all(english_ready(item, ('question', 'answer')) for item in items)
