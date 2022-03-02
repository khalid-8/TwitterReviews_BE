from django.apps import AppConfig


class TwitternlpConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'TwitterNLP'
    def ready(self):
        from Jobs import updater
        updater.start()