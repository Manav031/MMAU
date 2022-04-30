from django.apps import AppConfig


class BloodapiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bloodapi'

    def ready(self):
        import bloodapi.signals