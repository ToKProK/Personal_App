"""
URL configuration for Personal_App project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from os import name
from xml.dom.minidom import Document
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include

from Personal_App import settings
from . import views

app_name = "news" # ВАЖНО

urlpatterns = [
    path('news/add_news/', views.AddNewsPost.as_view(), name='add_news'),
    path('news/<slug:news_post_slug>/', views.NewsDetail.as_view(), name='show_news'),
    path('news/', views.NewsHome.as_view(), name='news'),
    path('news/edit/<slug:slug>/', views.EditNewsPost.as_view(), name='edit_news'),
    path('news/delete/<slug:slug>/', views.NewsDeleteView.as_view(), name='delete_news'),
]

if settings.DEBUG:  # Изображения
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)