from os import times_result
from tabnanny import verbose
from django.db import models
from django.urls import reverse

# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=News.Status.PUBLISHED)

class News(models.Model): # 23 Вид
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликованно'


    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,unique=True, db_index=True)
    content = models.TextField(blank=True)# blank=False - поле обязательно для заполнения
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(choices=Status.choices, default=Status.PUBLISHED) 

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title
    
    class Meta: # Сортировка БД через Django (р21)
        verbose_name = "Новости"#Название в админ панели 37 вид
        verbose_name_plural= "Новости"#Название в админ панели
        ordering = ['-time_create'] # Делаем сортировку по дате, сначала новые
        indexes = [
            models.Index(fields=['-time_create'])
        ]

    def get_absolute_url(self):
        return reverse("news:show_news", kwargs={"news_post_slug": self.slug}) #urls
    