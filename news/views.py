from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from re import template
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import permission_required

from news.forms import AddEditNewsForm
from .models import News

from django.core.paginator import Paginator

# Create your views here.
# def news(request): # Переход на страницу новостей
#     news_posts = News.published.all() # published это новый созданный менеджер, вместо objects
#     data = {
#         'news_posts' : news_posts,
#     }
#     return render(request, 'news.html', context=data)


class NewsHome(LoginRequiredMixin,ListView): # Переход на страницу новостей  #52
    model = News
    template_name = 'news/news.html'
    context_object_name = 'news_posts'
    paginate_by = 6 # Пагинация (страницы) # 58
    def get_queryset(self):
        return News.published.all()


class NewsDetail(LoginRequiredMixin,DetailView):  # Класс для отображения отдельной новости
    model = News
    template_name = 'news/news_post.html'
    context_object_name = 'news'
    slug_url_kwarg = 'news_post_slug'  # имя параметра из URL

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        context['cat_selected'] = 1
        return context




class AddNewsPost(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    form_class = AddEditNewsForm
    template_name = 'news/add_news.html'
    success_url = reverse_lazy('news:news')
    extra_context = {
        'title': "Добавление новости",
        'button': "Опубликовать",
    }
    # Присвоение автора к новости 63 вид 7:44
    # Функция вызвается если форма проверена и заполнена  
    def form_valid(self, form):
        news = form.save(commit=False)
        news.user = self.request.user
        news.save()  # теперь вызовется твой кастомный save() и сработает генерация slug

        messages.success(self.request, "Новость успешно добавлена!") 
        return redirect(self.success_url)
    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.is_staff or user.groups.filter(name='Руководитель').exists()


class EditNewsPost(LoginRequiredMixin,UserPassesTestMixin,UpdateView):

    model = News
    fields = ['title', 'content', 'photo', 'is_published']

    template_name = 'news/add_news.html'
    success_url = reverse_lazy('news:news')


    extra_context = {
        'title': "Редактирование новости",
        'button': "Сохранить",
    }
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Новость успешно обновлена!")
        return response
    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.is_staff or user.groups.filter(name='Руководитель').exists()


class NewsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = News
    success_url = reverse_lazy('news:news')

    def test_func(self):
        news = self.get_object()
        return (
            self.request.user == news.user or        # Автор
            self.request.user.is_superuser or        # Админ
            self.request.user.has_perm('news.delete_news')  # Редактор
        )
    def delete(self, request, *args, **kwargs):
        messages.success(request, "Новость успешно удалена!")
        return super().delete(request, *args, **kwargs)
    
    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.is_staff or user.groups.filter(name='Руководитель').exists()