from turtle import title
from django.contrib import admin
from .models import News
# Register your models here.

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'is_published')
    list_display_links = ('id', 'title')
#admin.site.register(News, NewsAdmin)

