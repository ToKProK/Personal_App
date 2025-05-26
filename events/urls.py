from os import name
from xml.dom.minidom import Document
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include

from Personal_App import settings
from . import views

app_name = "event" # ВАЖНО

urlpatterns = [
    path('events/', views.EventList.as_view(), name='events'),
]