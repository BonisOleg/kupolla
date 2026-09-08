from django.db import models


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(pk=self.pk).delete()
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class AboutPage(SingletonModel):
    mission_title = models.CharField('Заголовок місії', max_length=200, blank=True)
    mission_body = models.TextField('Текст місії', blank=True)
    values_body = models.TextField('Цінності', blank=True)
    cooperation_body = models.TextField('Етапи співпраці', blank=True)
    team_body = models.TextField('Команда', blank=True)
    cta_title = models.CharField('CTA заголовок', max_length=200, blank=True)

    class Meta:
        verbose_name = 'Сторінка «Про компанію»'
        verbose_name_plural = 'Сторінка «Про компанію»'

    def __str__(self):
        return 'Про компанію'


class TeamMember(models.Model):
    """Член команди KUPOLLA для секції «Команда» на сторінці «Про компанію»."""

    name = models.CharField('Ім\'я та прізвище', max_length=150)
    position = models.CharField('Посада', max_length=150)
    photo = models.ImageField('Фото', upload_to='team/', blank=True)
    order = models.PositiveSmallIntegerField('Порядок', default=0)
    is_published = models.BooleanField('Опубліковано', default=True)

    class Meta:
        verbose_name = 'Член команди'
        verbose_name_plural = 'Команда'
        ordering = ['order', 'pk']

    def __str__(self):
        return f'{self.name} — {self.position}'

    @property
    def initials(self):
        parts = self.name.split()
        return ''.join(p[0].upper() for p in parts[:2] if p)


class TechnologiesPage(SingletonModel):
    intro_body = models.TextField('Вступ', blank=True)
    construction_body = models.TextField('Конструктив куполу', blank=True)
    materials_body = models.TextField('Матеріали', blank=True)
    energy_body = models.TextField('Енергоефективність', blank=True)
    production_body = models.TextField('Виробництво та монтаж', blank=True)
    certificates_body = models.TextField('Сертифікати та гарантії', blank=True)

    class Meta:
        verbose_name = 'Сторінка «Технології»'
        verbose_name_plural = 'Сторінка «Технології»'

    def __str__(self):
        return 'Технології'
