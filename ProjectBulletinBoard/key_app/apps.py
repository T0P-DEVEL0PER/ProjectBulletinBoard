from django.apps import AppConfig


class KeyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'key_app'

    def ready(self):
        import key_app.signals
