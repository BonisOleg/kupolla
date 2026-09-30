from django.contrib import admin, messages
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, User
from django.core.exceptions import PermissionDenied
from django.db.models import QuerySet
from django.http import HttpRequest
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from src.core.admin_utils import SingletonModelAdminMixin

from .models import SiteSettings

if admin.site.is_registered(User):
    admin.site.unregister(User)
if admin.site.is_registered(Group):
    admin.site.unregister(Group)


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
        ('Мови на сайті', {
            'fields': (
                'en_enabled', 'sk_enabled', 'cs_enabled', 'nl_enabled',
                'ru_enabled', 'es_enabled', 'fr_enabled',
            ),
            'description': (
                'Українська завжди відкрита і без префікса в адресі. '
                'Увімкнена мова з’являється в перемикачі, hreflang і sitemap. '
                'Вимкнений префікс веде на українську версію тієї самої сторінки. '
                'Вкладки перекладу в адмінці лишаються для всіх мов.'
            ),
        }),
    )


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    def _blocked_delete_reason(self, request: HttpRequest, user: User) -> str | None:
        if user.pk == request.user.pk:
            return 'Не можна видалити власний обліковий запис.'
        if user.is_superuser and not (
            User.objects.filter(is_superuser=True).exclude(pk=user.pk).exists()
        ):
            return 'Не можна видалити останнього суперкористувача.'
        return None

    def has_delete_permission(self, request, obj=None):
        if obj is not None and self._blocked_delete_reason(request, obj):
            return False
        return super().has_delete_permission(request, obj)

    def delete_model(self, request, obj):
        reason = self._blocked_delete_reason(request, obj)
        if reason:
            messages.error(request, reason)
            raise PermissionDenied(reason)
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset: QuerySet[User]):
        users = list(queryset)
        blocked, allowed = [], []
        for user in users:
            if user.pk == request.user.pk:
                blocked.append((user, 'не можна видалити власний обліковий запис'))
            else:
                allowed.append(user)
        allowed_ids = {u.pk for u in allowed}
        supers_remaining = set(
            User.objects.filter(is_superuser=True)
            .exclude(pk__in=allowed_ids)
            .values_list('pk', flat=True)
        )
        if not supers_remaining:
            kept = []
            for user in allowed:
                if user.is_superuser:
                    blocked.append((user, 'не можна видалити останнього суперкористувача'))
                else:
                    kept.append(user)
            allowed = kept
        for user, reason in blocked:
            messages.warning(request, f'{user.username}: {reason}')
        if allowed:
            super().delete_queryset(request, queryset.filter(pk__in=[u.pk for u in allowed]))


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass
