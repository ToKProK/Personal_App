from django.shortcuts import get_object_or_404, redirect, render
from pkg_resources import parse_requirements

from django.contrib.auth.decorators import permission_required

from news.forms import AddNewsForm
from .models import News

from django.core.paginator import Paginator

# Create your views here.
def news(request): # Переход на страницу новостей
    news_posts = News.published.all() # published это новый созданный менеджер, вместо objects
    data = {
        'news_posts' : news_posts,
    }
    return render(request, 'news.html', context=data)

def show_news_post(request, news_post_slug): # Переход на конкретную новость
    news_post = get_object_or_404(News, slug=news_post_slug)
    data = {
        'title' : news_post.title,
        'news': news_post,
        'cat_selected': 1,
    }
    return render(request, 'news/news_post.html', data)

@permission_required(perm='news.add_news', raise_exception=True)
def addnews(request): # 44 VID
    parse_requirements = 'news.add_news'
    if request.method == "POST": # Если POST
        form = AddNewsForm(request.POST, request.FILES)
        if form.is_valid():
            news_item = form.save(commit=False)  # Не сохраняем сразу в БД
            news_item.user = request.user  # Устанавливаем текущего пользователя новости
            news_item.save()  # Теперь сохраняем с пользователем
            return redirect('news:news')
    else: # Если страница просто была запущенна
        form = AddNewsForm()
    data = {
        'title': "Добавление новости",
        'form':form
    }
    return render(request, 'news/add_news.html', data)