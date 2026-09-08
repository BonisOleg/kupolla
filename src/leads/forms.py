import re

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Lead


def validate_phone_number(value):
    phone = value.strip()
    digits = re.sub(r'\D', '', phone)
    if len(digits) < 10 or len(digits) > 15:
        raise ValidationError(_('Введіть коректний номер телефону'))
    if set(digits) == {'0'} or len(set(digits)) == 1:
        raise ValidationError(_('Введіть коректний номер телефону'))
    if digits.startswith('380'):
        if len(digits) != 12 or digits[3] == '0':
            raise ValidationError(_('Введіть коректний номер телефону'))
    elif digits.startswith('0'):
        if len(digits) != 10 or digits[1] == '0':
            raise ValidationError(_('Введіть коректний номер телефону'))
    elif digits[0] == '0':
        raise ValidationError(_('Введіть коректний номер телефону'))
    return phone


class LeadForm(forms.ModelForm):
    gdpr_consent = forms.BooleanField(
        required=True,
        label=_('Я погоджуюся з обробкою персональних даних'),
        error_messages={'required': _('Необхідно надати згоду на обробку даних')},
    )

    class Meta:
        model = Lead
        fields = ('form_type', 'name', 'phone', 'email', 'country', 'city', 'message', 'gdpr_consent',
                  'dome_model', 'equipment_tier', 'configurator_data')
        widgets = {
            'form_type': forms.HiddenInput(),
            'dome_model': forms.HiddenInput(),
            'equipment_tier': forms.HiddenInput(),
            'configurator_data': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'placeholder': _('Ваше ім\'я')})
        self.fields['phone'].widget.attrs.update({'placeholder': _('+380 XX XXX XX XX'), 'type': 'tel'})
        self.fields['email'].widget.attrs.update({'placeholder': _('email@example.com')})
        self.fields['country'].widget.attrs.update({'placeholder': _('Україна')})
        self.fields['city'].widget.attrs.update({'placeholder': _('Київ')})
        self.fields['message'].widget = forms.Textarea(attrs={'rows': 3, 'placeholder': _('Ваше повідомлення...')})

    def clean_phone(self):
        return validate_phone_number(self.cleaned_data.get('phone', ''))


class ContactForm(LeadForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['form_type'] = Lead.FormType.CONTACT


class HeroForm(LeadForm):
    class Meta(LeadForm.Meta):
        fields = ('form_type', 'name', 'phone', 'email', 'country', 'city', 'gdpr_consent')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['form_type'] = Lead.FormType.HERO


class ModelInquiryForm(LeadForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['form_type'] = Lead.FormType.MODEL
