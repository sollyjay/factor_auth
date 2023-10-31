from django.apps import AppConfig


class FactorappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'FactorApp'

    def ready(self):
        import FactorApp.signals
