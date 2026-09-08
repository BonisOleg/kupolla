from django.contrib import admin
from unfold.admin import ModelAdmin

from src.core.admin_utils import SingletonModelAdminMixin

from .models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonModelAdminMixin, ModelAdmin):
    fieldsets = (
        ('Контакти', {
            'fields': ('company_name', 'address', 'phone', 'phone_eu', 'email', 'working_hours'),
            'description': 'Контактні дані відображаються у шапці, футері та на сторінці контактів.',
        }),
        ('Реквізити', {
            'fields': ('company_code', 'vat_number'),
        }),
        ('Соціальні мережі та месенджери', {
            'fields': ('instagram', 'facebook', 'youtube', 'linkedin', 'telegram', 'whatsapp'),
        }),
        ('Інтеграції', {
            'fields': ('crm_webhook_url', 'ga4_measurement_id'),
            'description': 'CRM webhook отримує нові заявки автоматично. GA4 — для аналітики.',
        }),
        ('Карта та документи', {
            'fields': ('map_embed_url', 'google_drive_url', 'privacy_policy_url', 'terms_url'),
        }),
    )
