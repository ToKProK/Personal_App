from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    photo = models.ImageField(upload_to="users_avatar/", blank=True, null=True, verbose_name="Фотография")
    date_birth = models.DateField(blank=True, null=True, verbose_name="Дата рождения")
