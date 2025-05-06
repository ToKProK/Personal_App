import os
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.conf import settings
from .models import User

from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.core.files.storage import default_storage
import os
from .models import User


# ЭТО СКРИПТЫ, КОТОРЫЕ УДАЛЯЮТ ФОТОГРАФИИ, ПОСЛЕ ИХ ЗАМЕНЫ ИЛИ УДАЛЕНИЯ
@receiver(post_delete, sender=User)
def delete_old_photo(sender, instance, **kwargs):
    """Удаляем старое фото при удалении пользователя"""
    if instance.photo:
        try:
            # Получаем путь к файлу и удаляем его
            file_path = instance.photo.path
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Ошибка при удалении файла: {e}")

@receiver(pre_save, sender=User)
def delete_old_photo_before_update(sender, instance, **kwargs):
    """Удаляем старое фото перед обновлением профиля"""
    if instance.pk:
        old_instance = sender.objects.get(pk=instance.pk)
        if old_instance.photo and old_instance.photo != instance.photo:
            try:
                # Удаляем старое фото, если оно изменилось
                file_path = old_instance.photo.path
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Ошибка при удалении файла: {e}")
