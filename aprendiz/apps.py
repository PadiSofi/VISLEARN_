from django.apps import AppConfig

class AprendizConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'aprendiz'

    def ready(self):
        import aprendiz.signals