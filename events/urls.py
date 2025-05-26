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
    path('add/', views.AddEvent.as_view(), name='add_event'),
    path('events/<slug:event_slug>/', views.EventDetail.as_view(), name='event_detail'),
    path('events/edit/<slug:event_slug>/', views.EditEventPost.as_view(), name='edit_event'),
    path('events/delete/<slug:event_slug>/', views.EventDeleteView.as_view(), name='delete_event'),
]