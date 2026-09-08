from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Lead


@admin.action(description='Позначити як переглянуті')
def mark_leads_read(modeladmin, request, queryset):
    queryset.filter(status=Lead.Status.NEW).update(status=Lead.Status.READ)


@admin.action(description='Взяти в роботу')
def mark_leads_in_progress(modeladmin, request, queryset):
    queryset.update(status=Lead.Status.IN_PROGRESS)


@admin.action(description='Завершити')
def mark_leads_done(modeladmin, request, queryset):
    queryset.update(status=Lead.Status.DONE)


@admin.register(Lead)
class LeadAdmin(ModelAdmin):
    list_display = ('name', 'phone', 'email', 'city', 'country', 'form_type', 'dome_model', 'status', 'crm_sent', 'created_at')
    list_filter = ('form_type', 'status', 'crm_sent', 'country', 'created_at')
    list_filter_submit = True
    search_fields = ('name', 'phone', 'email', 'message', 'city', 'country')
    date_hierarchy = 'created_at'
    actions = (mark_leads_read, mark_leads_in_progress, mark_leads_done)
    list_editable = ('status',)
    autocomplete_fields = ('dome_model',)
    readonly_fields = (
        'form_type', 'name', 'phone', 'email', 'country', 'city', 'message', 'dome_model',
        'equipment_tier', 'configurator_data', 'ip_address', 'crm_sent', 'crm_sent_at', 'created_at',
    )

    fieldsets = (
        ('Контакти', {
            'fields': ('name', 'phone', 'email', 'country', 'city', 'form_type'),
        }),
        ('Деталі', {
            'fields': ('message', 'dome_model', 'equipment_tier', 'configurator_data'),
        }),
        ('Статус', {
            'fields': ('status', 'crm_sent', 'crm_sent_at'),
            'description': 'Заявки надходять з форм сайту — створювати вручну не можна.',
        }),
        ('Технічне', {
            'fields': ('ip_address', 'created_at'),
            'classes': ('collapse',),
        }),
    )

    def has_add_permission(self, request):
        return False
