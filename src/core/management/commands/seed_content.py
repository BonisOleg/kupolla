from django.core.management.base import BaseCommand

from src.blog.defaults import seed_blog
from src.catalog.defaults import seed_dome_images
from src.core.defaults import seed_site_settings, sync_site_settings_from_env
from src.pages.defaults import seed_pages


class Command(BaseCommand):
    help = 'Наповнює контент: зображення купола, блог, сторінки, SiteSettings (CRM з .env)'

    def handle(self, *args, **options):
        self.stdout.write('→ Зображення KUPOLLA (catalog)...')
        seed_dome_images()

        self.stdout.write('→ Блог...')
        seed_blog()

        self.stdout.write('→ Сторінки Про компанію / Технології...')
        seed_pages()

        self.stdout.write('→ SiteSettings + CRM webhook...')
        seed_site_settings()
        sync_site_settings_from_env()

        self.stdout.write(self.style.SUCCESS('Контент успішно наповнено.'))
