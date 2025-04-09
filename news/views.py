from django.shortcuts import get_object_or_404, render
from .models import News

# Create your views here.
def news(request):
    return render(request, 'news.html')

def show_news_post(request, news_post_id):
    news_post = get_object_or_404(News, pk=news_post_id)
    data = {
        'title' : news_post.title,
        'news': news_post,
        'cat_selected': 1,
    }
    return render(request, 'news/news_post.html', data)