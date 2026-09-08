from django.apps import AppConfig


class FaqConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.faq'
    verbose_name = 'FAQ'

    def ready(self):
        import src.faq.translation  # noqa: F401
