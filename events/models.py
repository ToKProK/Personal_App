from django.urls import reverse
from django.utils.text import slugify
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _\
#Переводим кирилицу в латиницу для slug
from transliterate import translit
from django.contrib.auth import get_user_model

class Event(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'
        CANCELLED = 2, 'Отменено'
        COMPLETED = 3, 'Завершено'


    class EventType(models.TextChoices):
        CONFERENCE = 'CONF', _('Конференция')
        SEMINAR = 'SEM', _('Семинар')
        WORKSHOP = 'WORK', _('Мастер-класс')
        EXHIBITION = 'EXH', _('Выставка')
        CONCERT = 'CONC', _('Концерт')
        VOLUNTEERING = 'VOL', _('Волонтёрская акция')
        CHARITY = 'CHAR', _('Благотворительное мероприятие')
        ECOLOGY = 'ECO', _('Экологическая акция')
        CAREER = 'CAREER', _('Карьерное консультирование')
        SOCIAL = 'SOC', _('Социальное взаимодействие')
        CULTURE = 'CULT', _('Культурное мероприятие')
        OTHER = 'OTH', _('Другое')

    # Основная информация
    title = models.CharField(max_length=255, verbose_name="Название мероприятия")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    description = models.TextField(blank=True, verbose_name="Описание")
    event_type = models.CharField(
        max_length=8,
        choices=EventType.choices,
        default=EventType.OTHER,
        verbose_name="Тип мероприятия"
    )
    
    # Даты и время
    start_datetime = models.DateTimeField(verbose_name="Дата и время начала")
    end_datetime = models.DateTimeField(verbose_name="Дата и время окончания")
    registration_deadline = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Крайний срок регистрации"
    )
    
    # Место проведения
    location = models.CharField(max_length=255, verbose_name="Место проведения")
    address = models.TextField(blank=True, null=True,verbose_name="Адрес")
    online_event = models.BooleanField(default=False, verbose_name="Онлайн-мероприятие")
    online_link = models.URLField(blank=True, null=True, verbose_name="Ссылка для онлайн-участия")
    
    # Организационная информация
    organizer = models.CharField(max_length=255, verbose_name="Организатор")
    contact_email = models.EmailField(verbose_name="Контактный email")
    contact_phone = models.CharField(max_length=20, blank=True, verbose_name="Контактный телефон")
    
    # Визуальные элементы
    image = models.ImageField(
        upload_to="events/%Y/",
        blank=True,
        null=True,
        #verbose_name - читаемое название в админке
        verbose_name="Фото"
    )
    
    # Настройки
    #Значение по умолчанию
    is_published = models.BooleanField(
        choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
        default=Status.PUBLISHED,
        verbose_name="Статус"
    )
    
    # Системные поля
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")   # Автоматически при создании
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")  # Автоматически при обновлении
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL, # При удалении пользователя поле станет NULL
        null=True,
        related_name='created_events',  # Обратная связь: user.created_events.all()
        verbose_name="Создатель"
    )
    
    class Meta:
        verbose_name = "Мероприятие" # Название в единственном числе
        verbose_name_plural = "Мероприятия" # Название во множественном числе
        ordering = ['-start_datetime']   # Сортировка по умолчанию
        indexes = [  # Индексы для ускорения запросов
            models.Index(fields=['start_datetime']),
            models.Index(fields=['is_published']),
            models.Index(fields=['event_type']),
        ]
    
    def get_absolute_url(self):
        return reverse("events:event_detail", kwargs={"event_slug": self.slug}) #urls

    def __str__(self):
        return f"{self.title} ({self.get_event_type_display()})"   # Отображение в админке
    
    @property
    def is_upcoming(self):
        from django.utils import timezone
        return self.start_datetime > timezone.now() # True если мероприятие в будущем
    
    @property
    def duration(self):
        return self.end_datetime - self.start_datetime # Длительность мероприятия
    
    def save(self, *args, **kwargs):
        if not self.slug:
            if self.title:
                # Транслитерируем кириллицу в латиницу
                slug_base = translit(self.title, 'ru', reversed=True)
                self.slug = slugify(slug_base)
            else:
                import uuid
                self.slug = str(uuid.uuid4())[:8]

            original_slug = self.slug
            counter = 1
            while Event.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)


class Subscribe(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='subscribe') #чтобы из пользователя можно было получить все регистрации через user.registrations.all().
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='subscribes')  
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')  # чтобы один пользователь не мог зарегистрироваться дважды

    def __str__(self):
        return f"{self.user} зарегистрирован на {self.event.title}"