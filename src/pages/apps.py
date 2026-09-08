from django.apps import AppConfig


class PagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.pages'
    verbose_name = 'Статичні сторінки'

    def ready(self):
        import src.pages.translation  # noqa: F401
