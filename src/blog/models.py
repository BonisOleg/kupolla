from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField('Назва', max_length=100)
    slug = models.SlugField('Slug', unique=True, blank=True)

    class Meta:
        verbose_name = 'Категорія блогу'
        verbose_name_plural = 'Категорії блогу'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField('Назва', max_length=50)
    slug = models.SlugField('Slug', unique=True, blank=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Post(models.Model):
    title = models.CharField('Заголовок', max_length=255)
    slug = models.SlugField('Slug', unique=True, blank=True)
    excerpt = models.TextField('Анонс', max_length=500, blank=True)
    body = models.TextField('Контент (HTML)')
    cover_image = models.ImageField('Обкладинка', upload_to='blog/', blank=True)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True,
                                  verbose_name='Категорія', related_name='posts')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='Теги')

    seo_title = models.CharField('SEO заголовок', max_length=70, blank=True)
    seo_description = models.CharField('SEO опис', max_length=160, blank=True)

    is_published = models.BooleanField('Опубліковано', default=False)
    published_at = models.DateTimeField('Дата публікації', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Стаття'
        verbose_name_plural = 'Статті'
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post', kwargs={'slug': self.slug})
