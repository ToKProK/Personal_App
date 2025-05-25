
from django.contrib import admin, messages
from .models import News
# Register your models here.

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    fields = ['title', 'content' ]
    readonly_fields = ['slug']
    list_display = ('title', 'time_create', 'is_published', "slug", 'count_info')
    list_display_links = ('title',)
    list_editable = ('is_published', )
    actions = ['set_published', 'set_draft']

    @admin.display(description="Краткое описание")
    def count_info(self, single_news : News):
        return f"Описание {len(single_news.content)} символов."
    
    @admin.action(description='Опубликовать выбранные записи')
    def set_published(self, request, queryset):
        update = queryset.update(is_published=News.Status.PUBLISHED)
        self.message_user(request, f"Изменено {update} записей. ")


    @admin.action(description='Снять с публикации выбранные записи')
    def set_draft(self, request, queryset):
        update = queryset.update(is_published=News.Status.DRAFT)
        self.message_user(request, f"Изменено {update} записей.", messages.WARNING)

#admin.site.register(News, NewsAdmin)

 