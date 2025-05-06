from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    def ready(self): # Это необходимо для того, чтобы сигналы работали при старте приложения. Они находятся в signals.py 
        import news.signals