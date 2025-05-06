from os import times_result
from tabnanny import verbose
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from users.forms import User
# Create your models here.

def translit_to_eng(value: str) -> str:
    translit_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
        'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
    }
    return "".join(map(lambda x: translit_dict[x] if translit_dict.get(x, False) else x, value.lower()))


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=News.Status.PUBLISHED)

class News(models.Model): # 23 Вид
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликованно'


    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255,unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name="Описание")# blank=False - поле обязательно для заполнения
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)), default=Status.PUBLISHED, verbose_name="Статус") #38
    photo = models.ImageField(upload_to="news_photos/%Y/", default=None, blank=True, null=True, verbose_name="Фото")
    objects = models.Manager()
    published = PublishedManager()
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)

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
    
    # def save(self, *args, **kwargs): # При сохранании будет автоматический создаваться slug
    #     self.slug = slugify(translit_to_eng(self.title))
    #     super().save(*args, **kwargs)

    def save(self, *args, **kwargs): # При сохранании будет автоматический создаваться slug
        # Берем первые 5 букв из content (если они есть)
        content_part = self.content[:5] if self.content else ''
        # Объединяем title и первые 5 букв content
        slug_source = f"{self.title} {content_part}"
        self.slug = slugify(translit_to_eng(slug_source))
        super().save(*args, **kwargs)


class UploadFiles(models.Model):
    file = models.FileField(upload_to='image_uploads')