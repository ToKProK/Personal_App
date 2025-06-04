import os
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from django.core.files.storage import default_storage
from .models import Event


# ЭТО СКРИПТЫ, КОТОРЫЕ УДАЛЯЮТ ФОТОГРАФИИ, ПОСЛЕ ИХ ЗАМЕНЫ ИЛИ УДАЛЕНИЯ
@receiver(post_delete, sender=Event)
def delete_old_image(sender, instance, **kwargs):
    """Удаляем старое фото при удалении мероприятия"""
    if instance.image:
        try:
            file_path = instance.image.path
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Ошибка при удалении файла: {e}")

@receiver(pre_save, sender=Event)
def delete_old_image_before_update(sender, instance, **kwargs):
    """Удаляем старое фото перед обновлением мероприятия"""
    if instance.pk:
        old_instance = sender.objects.get(pk=instance.pk)
        if old_instance.image and old_instance.image != instance.image:
            try:
                file_path = old_instance.image.path
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Ошибка при удалении файла: {e}")
