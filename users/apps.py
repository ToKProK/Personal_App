from django.apps import AppConfig
from django.db.models.signals import post_migrate
class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self): # Это необходимо для того, чтобы сигналы работали при старте приложения. Они находятся в signals.py 
        import users.signals


def create_default_groups(sender, **kwargs):
    from django.contrib.auth.models import Group  # Импорт внутри функции, чтобы избежать ошибки
    groups = ['Руководитель', 'Волонтёр', 'Участник']
    for group_name in groups:
        Group.objects.get_or_create(name=group_name)

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        post_migrate.connect(create_default_groups, sender=self)