from django.apps import AppConfig

class SimplimsAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "simplims_app"

    def ready(self):
        import simplims_app.signals
