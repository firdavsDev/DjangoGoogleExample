from django.apps import AppConfig


class GoogleCustomAutConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "google_custom_aut"

    def ready(self):
        import google_custom_aut.signals  # noqa
