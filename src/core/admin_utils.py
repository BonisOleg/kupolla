"""Спільні mixins для django-unfold адмінки."""

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from tinymce.widgets import TinyMCE

from .image_specs import IMAGE_FORMAT_HINT


class SingletonModelAdminMixin:
    """Singleton: changelist → редагування єдиного запису pk=1."""

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def changelist_view(self, request, extra_context=None):
        obj, _ = self.model.objects.get_or_create(pk=1)
        meta = self.model._meta
        url_name = f'admin:{meta.app_label}_{meta.model_name}_change'
        return HttpResponseRedirect(reverse(url_name, args=[obj.pk]))


class TinyMCEAdminMixin:
    """TinyMCE для rich-text полів, включно з modeltranslation (_uk, _en…)."""

    tinymce_fields = ()

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        name = db_field.name
        for base in self.tinymce_fields:
            if name == base or name.startswith(f'{base}_'):
                kwargs['widget'] = TinyMCE(attrs={'cols': 80, 'rows': 30})
                break
        return super().formfield_for_dbfield(db_field, request, **kwargs)


class ImageSizeHelpMixin:
    """Додає help_text з рекомендованим розміром до ImageField."""

    image_size_help = {}

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        size_hint = self.image_size_help.get(db_field.name)
        if size_hint and hasattr(field, 'help_text'):
            parts = [size_hint, IMAGE_FORMAT_HINT]
            if field.help_text:
                parts.insert(0, str(field.help_text))
            field.help_text = ' '.join(parts)
        return field


class ImagePreviewMixin:
    """HTML-превʼю ImageField для list_display та readonly_fields."""

    image_field = 'image'
    preview_height = 60
    preview_label = 'Превʼю'

    def get_image_preview(self, obj):
        field = getattr(obj, self.image_field, None)
        if field:
            return format_html(
                '<img src="{}" alt="" style="height:{}px;border-radius:4px;object-fit:cover;">',
                field.url,
                self.preview_height,
            )
        return '—'

    get_image_preview.short_description = preview_label


def english_ready(obj, fields) -> bool:
    """Чи заповнені англійські переклади перелічених полів."""
    for field in fields:
        if not (getattr(obj, f'{field}_en', '') or '').strip():
            return False
    return True


def image_size_notice(*lines):
    """Текст для description fieldset з рекомендаціями."""
    return ' '.join(lines)
