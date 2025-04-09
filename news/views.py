from django.shortcuts import get_object_or_404, render
from .models import News

# Create your views here.
def news(request):
    news_posts = News.published.all() # published это новый созданный менеджер, вместо objects
    data = {
        'news_posts' : news_posts
    }
    return render(request, 'news.html', context=data)

def show_news_post(request, news_post_slug):
    news_post = get_object_or_404(News, slug=news_post_slug)
    data = {
        'title' : news_post.title,
        'news': news_post,
        'cat_selected': 1,
    }
    return render(request, 'news/news_post.html', data)
