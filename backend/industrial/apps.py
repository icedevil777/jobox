from django.apps import AppConfig


class IndustrialConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'industrial'

    def ready(self):
        from industrial import model_signals
