from django.apps import AppConfig


class LivestreamConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'livestream'

    def ready(self):
        import livestream.signals  # Import signals after app is ready
