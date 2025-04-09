from os import times_result
from django.db import models

# Create your models here.

class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)# blank=False - поле обязательно для заполнения
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
    class Meta: # Сортировка БД через Django (р21)
        ordering = ['-time_create'] # Делаем сортировку по дате, сначала новые
        indexes = [
            models.Index(fields=['-time_create'])
        ]