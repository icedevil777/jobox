from django.apps import AppConfig


class PaymentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payment'

    def ready(self):
        try:
            import payment.model_signals  # noqa F401
        except ImportError:
            pass
