from .models import Event
from django.shortcuts import render
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
# Create your views here.

class EventList(ListView): # Переход на страницу новостей  #52
    model = Event
    template_name = 'events/events_list.html'
    context_object_name = 'events'
    paginate_by = 6 # Пагинация (страницы) # 58
    # def get_queryset(self):
    #     return Event.published.all()