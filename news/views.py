from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from re import template
from django.shortcuts import get_object_or_404, redirect, render
from pkg_resources import parse_requirements
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


class NewsHome(ListView): # Переход на страницу новостей  #52
    model = News
    template_name = 'news/news.html'
    context_object_name = 'news_posts'
    paginate_by = 6 # Пагинация (страницы) # 58
    def get_queryset(self):
        return News.published.all()
    
def show_news_post(request, news_post_slug): # Переход на конкретную новость
    news_post = get_object_or_404(News, slug=news_post_slug)
    data = {
        'title' : news_post.title,
        'news': news_post,
        'cat_selected': 1,
    }
    return render(request, 'news/news_post.html', data)






# @permission_required(perm='news.add_news', raise_exception=True)
# def addnews(request): # 44 VID
#     parse_requirements = 'news.add_news'
#     if request.method == "POST": # Если POST
#         form = AddNewsForm(request.POST, request.FILES)
#         if form.is_valid():
#             news_item = form.save(commit=False)  # Не сохраняем сразу в БД
#             news_item.user = request.user  # Устанавливаем текущего пользователя новости
#             news_item.save()  # Теперь сохраняем с пользователем
#             return redirect('news:news')
#     else: # Если страница просто была запущенна
#         form = AddNewsForm()
#     data = {

#         'form':form
#     }
#     return render(request, 'news/add_news.html', data)


#@permission_required(perm='news.add_news', raise_exception=True)
class AddNewsPost(CreateView):
    form_class = AddEditNewsForm
    template_name = 'news/add_news.html'
    success_url = reverse_lazy('news:news')
    extra_context = {
        'title': "Добавление новости",
    }
    # Присвоение автора к новости 63 вид 7:44
    # Функция вызвается если форма проверена и заполнена  
    def form_valid(self, form):
        # Создадим объект новой записи (без добаление в бд)
        w = form.save(commit=False)
        # получение текущего пользоватьеля и происвоение его новости
        w.user = self.request.user
        
        return super().form_valid(form)


class EditNewsPost(UpdateView):

    model = News
    fields = ['title', 'content', 'photo', 'is_published']

    template_name = 'news/add_news.html'
    success_url = reverse_lazy('news:news')


    extra_context = {
        'title': "Редактирование новости",
    }


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