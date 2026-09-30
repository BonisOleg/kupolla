from django import forms
from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin
from unfold.widgets import UnfoldAdminTextareaWidget

from src.core.admin_utils import english_ready

from .models import ConfigOption


class FeatureListField(forms.CharField):
    """Список особливостей: один рядок — один пункт, у моделі лишається список рядків."""

    widget = UnfoldAdminTextareaWidget

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('required', False)
        kwargs.setdefault('label', 'Особливості')
        kwargs.setdefault('help_text', 'Кожна особливість — з нового рядка.')
        super().__init__(*args, **kwargs)
        self.widget.attrs.setdefault('rows', 6)

    def prepare_value(self, value):
        if isinstance(value, list):
            return '\n'.join(str(item) for item in value)
        if value in (None, ''):
            return ''
        return value

    def to_python(self, value):
        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]
        if value in (None, ''):
            return []
        return [line.strip() for line in str(value).splitlines() if line.strip()]


class ConfigOptionAdminForm(forms.ModelForm):
    features = FeatureListField()

    class Meta:
        model = ConfigOption
        fields = '__all__'


@admin.register(ConfigOption)
class ConfigOptionAdmin(TabbedTranslationAdmin, ModelAdmin):
    form = ConfigOptionAdminForm
    list_display = ('name', 'option_type', 'code', 'en_ready', 'base_price', 'price_delta', 'is_popular', 'is_active', 'order')
    en_fields = ('name',)
    list_editable = ('is_active', 'is_popular', 'order', 'base_price', 'price_delta')
    list_filter = ('option_type', 'is_active')
    list_filter_submit = True
    search_fields = ('name', 'code')
    ordering = ('option_type', 'order')

    @admin.display(boolean=True, description='EN')
    def en_ready(self, obj):
        return english_ready(obj, self.en_fields)

    fieldsets = (
        ('Основне', {
            'fields': ('name', 'code', 'option_type', 'is_active', 'is_popular', 'order'),
            'description': 'Код — унікальний ідентифікатор для калькулятора (латиниця, без пробілів).',
        }),
        ('Ціни (€)', {
            'fields': ('base_price', 'price_delta'),
            'description': 'base_price — для типу «Базова модель»; price_delta — додаткова вартість для tier/addon.',
        }),
        ('Особливості', {
            'fields': ('features',),
            'description': 'Список переваг комплектації — показується в конфігураторі. Один рядок — один пункт.',
        }),
    )
