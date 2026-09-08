from django.db import models


class FAQGroup(models.Model):
    name = models.CharField('Тема', max_length=100)
    order = models.PositiveSmallIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Група FAQ'
        verbose_name_plural = 'Групи FAQ'
        ordering = ['order']

    def __str__(self):
        return self.name


class FAQItem(models.Model):
    group = models.ForeignKey(FAQGroup, on_delete=models.CASCADE, related_name='items', verbose_name='Група')
    question = models.CharField('Питання', max_length=300)
    answer = models.TextField('Відповідь')
    order = models.PositiveSmallIntegerField('Порядок', default=0)
    is_published = models.BooleanField('Опубліковано', default=True)

    class Meta:
        verbose_name = 'Питання FAQ'
        verbose_name_plural = 'Питання FAQ'
        ordering = ['order']

    def __str__(self):
        return self.question[:80]
