from django.apps import AppConfig


class GalleryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.gallery'
    verbose_name = 'Галерея'

    def ready(self):
        import src.gallery.translation  # noqa: F401
