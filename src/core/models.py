from django.db import models
from django.db.models import ProtectedError


class SingletonQuerySet(models.QuerySet):
    def delete(self):
        if not self.exists():
            return 0, {}
        raise ProtectedError('Єдиний запис видаляти не можна.', set(self))


class SingletonModel(models.Model):
    """Єдиний запис: завжди pk=1, видалення заборонене."""

    objects = SingletonQuerySet.as_manager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ProtectedError('Єдиний запис видаляти не можна.', {self})

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class SiteSettings(SingletonModel):
    address = models.CharField('Адреса', max_length=255, blank=True)
    phone = models.CharField('Телефон (Україна)', max_length=30, blank=True)
    phone_eu = models.CharField('Телефон (Європа та інші країни)', max_length=30, blank=True)
    email = models.EmailField('Email', blank=True)
    working_hours = models.CharField('Графік роботи', max_length=100, blank=True)

    crm_webhook_url = models.URLField('CRM Webhook URL', blank=True)
    ga4_measurement_id = models.CharField('GA4 Measurement ID', max_length=50, blank=True)

    instagram = models.URLField('Instagram', blank=True)
    facebook = models.URLField('Facebook', blank=True)
    youtube = models.URLField('YouTube', blank=True)
    linkedin = models.URLField('LinkedIn', blank=True)
    telegram = models.URLField('Telegram', blank=True)
    whatsapp = models.URLField('WhatsApp', blank=True)

    company_name = models.CharField('Назва компанії', max_length=100, default='KUPOLLA')
    company_code = models.CharField('Код ЄДРПОУ', max_length=20, blank=True)
    vat_number = models.CharField('ПДВ / ІПН', max_length=20, blank=True)

    map_embed_url = models.URLField('URL карти (embed)', blank=True,
                                    help_text='OpenStreetMap або Google Maps embed URL')
    privacy_policy_url = models.CharField('URL Політики конфіденційності', max_length=255, blank=True)
    terms_url = models.CharField('URL Умов використання', max_length=255, blank=True)
    google_drive_url = models.URLField(
        'Посилання на Google Drive',
        blank=True,
        help_text='Матеріали / фото для сторінки Контакти',
    )

    en_enabled = models.BooleanField('English на сайті', default=True)
    sk_enabled = models.BooleanField('Slovenčina на сайті', default=False)
    cs_enabled = models.BooleanField('Čeština на сайті', default=False)
    nl_enabled = models.BooleanField('Nederlands на сайті', default=False)
    ru_enabled = models.BooleanField('Русский на сайті', default=False)
    es_enabled = models.BooleanField('Español на сайті', default=False)
    fr_enabled = models.BooleanField('Français на сайті', default=False)

    class Meta:
        verbose_name = 'Налаштування сайту'
        verbose_name_plural = 'Налаштування сайту'
        constraints = [
            models.CheckConstraint(
                condition=models.Q(pk=1),
                name='core_sitesettings_singleton_pk',
            ),
        ]

    def __str__(self):
        return 'Налаштування сайту'
