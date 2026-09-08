from django.db import models


class GalleryPhoto(models.Model):
    class ProjectType(models.TextChoices):
        GLAMPING = 'glamping', 'Глемпінг'
        LIVING = 'living', 'Проживання'
        COMMERCIAL = 'commercial', 'Комерція'

    class Category(models.TextChoices):
        DOME = 'dome', 'Купол'
        PRODUCTION = 'production', 'Виробництво'

    title = models.CharField('Підпис', max_length=200, blank=True)
    image = models.ImageField('Фото', upload_to='gallery/')
    alt = models.CharField('Alt текст', max_length=200, blank=True)
    category = models.CharField('Блок галереї', max_length=20, choices=Category.choices, default=Category.DOME)
    project_type = models.CharField('Тип проєкту', max_length=20, choices=ProjectType.choices, default=ProjectType.LIVING)
    order = models.PositiveSmallIntegerField('Порядок', default=0)
    is_published = models.BooleanField('Опубліковано', default=True)

    class Meta:
        verbose_name = 'Фото галереї'
        verbose_name_plural = 'Галерея'
        ordering = ['order', '-pk']

    def __str__(self):
        return self.title or f'Photo #{self.pk}'
