from django.apps import AppConfig


class VacayvueConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'VacayVue'
# apps.py
    def ready(self):
        import VacayVue.signals  # Import signals module when the app is ready
