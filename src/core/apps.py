from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.core'
    verbose_name = 'Налаштування сайту'

    def ready(self):
        from src.core.image_compress import connect_image_compress_signals

        connect_image_compress_signals()
