from django import forms
from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin

from .models import ConfigOption


class ConfigOptionAdminForm(forms.ModelForm):
    features = forms.JSONField(
        required=False,
        help_text='JSON-масив рядків, напр.: ["Утеплення 200 мм", "Панорамне вікно"].',
        widget=forms.Textarea(attrs={'rows': 4, 'style': 'font-family: monospace;'}),
    )

    class Meta:
        model = ConfigOption
        fields = '__all__'

    def clean_features(self):
        value = self.cleaned_data.get('features')
        if value is None:
            return []
        if not isinstance(value, list):
            raise forms.ValidationError('Особливості мають бути JSON-масивом рядків, напр. ["Пункт 1", "Пункт 2"].')
        if not all(isinstance(item, str) for item in value):
            raise forms.ValidationError('Кожен елемент масиву features має бути текстовим рядком.')
        return value


@admin.register(ConfigOption)
class ConfigOptionAdmin(TabbedTranslationAdmin, ModelAdmin):
    form = ConfigOptionAdminForm
    list_display = ('name', 'option_type', 'code', 'base_price', 'price_delta', 'is_popular', 'is_active', 'order')
    list_editable = ('is_active', 'is_popular', 'order', 'base_price', 'price_delta')
    list_filter = ('option_type', 'is_active')
    list_filter_submit = True
    search_fields = ('name', 'code')
    ordering = ('option_type', 'order')

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
            'description': 'Список переваг комплектації — показується в конфігураторі.',
        }),
    )
