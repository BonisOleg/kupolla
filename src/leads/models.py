from django.db import models


class Lead(models.Model):
    class FormType(models.TextChoices):
        HERO = 'hero', 'CTA Головна (hero)'
        CONTACT = 'contact', 'Контакти'
        ABOUT = 'about', 'Про компанію'
        MODEL = 'model', 'Заявка на модель'
        CONFIGURATOR = 'configurator', 'Конфігуратор'
        FAQ = 'faq', 'FAQ fallback'

    class Status(models.TextChoices):
        NEW = 'new', 'Нова'
        READ = 'read', 'Переглянута'
        IN_PROGRESS = 'in_progress', 'В роботі'
        DONE = 'done', 'Завершена'

    form_type = models.CharField('Тип форми', max_length=20, choices=FormType.choices, default=FormType.CONTACT)
    name = models.CharField('Ім\'я', max_length=150)
    phone = models.CharField('Телефон', max_length=30)
    email = models.EmailField('Email', blank=True)
    country = models.CharField('Країна', max_length=100, blank=True)
    city = models.CharField('Місто', max_length=100, blank=True)
    message = models.TextField('Повідомлення', blank=True)
    gdpr_consent = models.BooleanField('Згода GDPR', default=False)

    dome_model = models.ForeignKey(
        'catalog.DomeModel',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name='Модель куполу',
        related_name='leads',
    )
    equipment_tier = models.CharField('Комплектація', max_length=20, blank=True)
    configurator_data = models.JSONField('Дані конфігуратора', null=True, blank=True)

    status = models.CharField('Статус', max_length=20, choices=Status.choices, default=Status.NEW)
    crm_sent = models.BooleanField('Відправлено до CRM', default=False)
    crm_sent_at = models.DateTimeField('Дата відправки до CRM', null=True, blank=True)

    ip_address = models.GenericIPAddressField('IP адреса', null=True, blank=True)
    created_at = models.DateTimeField('Дата заявки', auto_now_add=True)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.get_form_type_display()} — {self.name} ({self.created_at.strftime("%d.%m.%Y")})'
