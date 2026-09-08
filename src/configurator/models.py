from django.db import models


class ConfigOption(models.Model):
    class OptionType(models.TextChoices):
        MODEL = 'model', 'Базова модель'
        DIAMETER = 'diameter', 'Діаметр'
        TIER = 'tier', 'Комплектація'
        ADDON = 'addon', 'Опція (додатково)'

    option_type = models.CharField('Тип опції', max_length=20, choices=OptionType.choices)
    code = models.SlugField('Код', unique=True)
    name = models.CharField('Назва', max_length=100)
    price_delta = models.DecimalField('Надбавка, €', max_digits=10, decimal_places=0, default=0)
    base_price = models.DecimalField('Базова ціна, €', max_digits=10, decimal_places=0, default=0)
    features = models.JSONField('Особливості', default=list, blank=True)
    is_popular = models.BooleanField('Популярна', default=False)
    is_active = models.BooleanField('Активно', default=True)
    order = models.PositiveSmallIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Опція конфігуратора'
        verbose_name_plural = 'Опції конфігуратора'
        ordering = ['option_type', 'order']

    def __str__(self):
        return f'[{self.get_option_type_display()}] {self.name}'
