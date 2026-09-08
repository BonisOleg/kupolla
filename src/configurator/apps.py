from django.apps import AppConfig


class ConfiguratorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.configurator'
    verbose_name = 'Конфігуратор'

    def ready(self):
        import src.configurator.translation  # noqa: F401
