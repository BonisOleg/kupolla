from django.apps import AppConfig


class CatalogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.catalog'
    verbose_name = 'KUPOLLA'

    def ready(self):
        import src.catalog.translation  # noqa: F401
