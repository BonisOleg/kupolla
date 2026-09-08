from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class DomeModel(models.Model):
    class Purpose(models.TextChoices):
        LIVING = 'living', 'Проживання'
        GLAMPING = 'glamping', 'Глемпінг'
        COMMERCIAL = 'commercial', 'Комерція'

    class SizeCategory(models.TextChoices):
        SMALL = 'small', 'Малий'
        MEDIUM = 'medium', 'Середній'
        LARGE = 'large', 'Великий'

    name = models.CharField('Назва', max_length=100)
    slug = models.SlugField('Slug', unique=True, blank=True)
    area_m2 = models.PositiveIntegerField('Площа, м²')
    diameter = models.DecimalField('Діаметр, м', max_digits=5, decimal_places=1)
    height_m = models.DecimalField('Висота, м', max_digits=4, decimal_places=1)
    insulation_mm = models.PositiveIntegerField('Утеплення, мм', default=200)

    purpose = models.CharField('Призначення', max_length=20, choices=Purpose.choices, default=Purpose.LIVING)
    size_cat = models.CharField('Розмір', max_length=10, choices=SizeCategory.choices, default=SizeCategory.MEDIUM)

    description = models.TextField('Опис', blank=True)
    short_description = models.CharField('Короткий опис', max_length=255, blank=True)
    floor_plan_image = models.ImageField(
        'Планування (зображення)',
        upload_to='catalog/plans/',
        blank=True,
        null=True,
    )
    floor_plan_note = models.TextField('Планування (опис/схема)', blank=True)

    price_base = models.DecimalField('Ціна Базова, €', max_digits=10, decimal_places=0, null=True, blank=True)
    price_standard = models.DecimalField('Ціна Стандарт, €', max_digits=10, decimal_places=0, null=True, blank=True)
    price_premium = models.DecimalField('Ціна Преміум, €', max_digits=10, decimal_places=0, null=True, blank=True)

    is_published = models.BooleanField('Опубліковано', default=False)
    is_featured = models.BooleanField('Показувати на головній', default=False)
    order = models.PositiveSmallIntegerField('Порядок', default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Модель куполу'
        verbose_name_plural = 'Моделі куполів'
        ordering = ['order', 'area_m2']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('catalog:detail', kwargs={'slug': self.slug})

    @property
    def price_from(self):
        prices = [p for p in [self.price_base, self.price_standard, self.price_premium] if p]
        return min(prices) if prices else None


class ModelImage(models.Model):
    dome = models.ForeignKey(DomeModel, on_delete=models.CASCADE, related_name='images', verbose_name='Модель')
    image = models.ImageField('Зображення', upload_to='catalog/')
    alt = models.CharField('Alt текст', max_length=200, blank=True)
    is_main = models.BooleanField('Головне', default=False)
    order = models.PositiveSmallIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Зображення моделі'
        verbose_name_plural = 'Зображення моделей'
        ordering = ['-is_main', 'order']

    def __str__(self):
        return f'{self.dome.name} — {self.order}'

    def save(self, *args, **kwargs):
        if self.is_main:
            ModelImage.objects.filter(dome=self.dome, is_main=True).exclude(pk=self.pk).update(is_main=False)
        super().save(*args, **kwargs)


class ModelSpec(models.Model):
    dome = models.ForeignKey(DomeModel, on_delete=models.CASCADE, related_name='specs', verbose_name='Модель')
    key = models.CharField('Характеристика', max_length=100)
    value = models.CharField('Значення', max_length=200)
    order = models.PositiveSmallIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'
        ordering = ['order']

    def __str__(self):
        return f'{self.key}: {self.value}'
