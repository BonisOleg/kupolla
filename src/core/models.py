from django.db import models


class SingletonModel(models.Model):
    """Базовий клас для singleton-моделей (лише один запис)."""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(pk=self.pk).delete()
        super().save(*args, **kwargs)

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

    class Meta:
        verbose_name = 'Налаштування сайту'
        verbose_name_plural = 'Налаштування сайту'

    def __str__(self):
        return 'Налаштування сайту'
