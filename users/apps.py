from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self): # Это необходимо для того, чтобы сигналы работали при старте приложения. Они находятся в signals.py 
        import users.signals
