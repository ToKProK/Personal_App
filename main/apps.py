from django.apps import AppConfig
from django.db.models.signals import post_migrate

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        post_migrate.connect(create_default_groups, sender=self)

        
def create_default_groups(sender, **kwargs):
    from django.contrib.auth.models import Group  # Импорт внутри функции, чтобы избежать ошибки
    groups = ['Руководитель', 'Волонтёр', 'Участник']
    for group_name in groups:
        Group.objects.get_or_create(name=group_name)
