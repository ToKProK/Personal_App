from django.urls import reverse, reverse_lazy
from django.views import View
from events.forms import AddEditEventForm
from .models import Event, Subscribe
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# Create your views here.

class EventList(ListView): # Переход на страницу новостей  #52
    model = Event
    template_name = 'events/events_list.html'
    context_object_name = 'events'
    paginate_by = 6 # Пагинация (страницы) # 58



class EventDetail(DeleteView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'
    slug_url_kwarg = 'event_slug'  # имя параметра из URL

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        # Можно добавить дополнительные данные в контекст
        context['is_upcoming'] = self.object.is_upcoming


        # проверка подписки 
        if self.request.user.is_authenticated:
            context['user_subscribed'] = self.object.subscribes.filter(user=self.request.user).exists()
        else:
            context['user_subscribed'] = False


        
        context['subscribed_users'] = self.object.subscribes.select_related('user').all()
        return context
    



class AddEvent(CreateView):
    form_class = AddEditEventForm
    template_name = 'events/add_event.html'
    success_url = reverse_lazy('events:events')
    extra_context = {
        'title': "Добавление мероприятия",
        'button':'Создать мероприятие'
    }
    def form_valid(self, form):
        event = form.save(commit=False)
        event.created_by = self.request.user
        event.save()
        return redirect(self.success_url)
    
class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event  # НЕ вызываем Event(), просто указываем класс модели
    template_name = 'events/event_confirm_delete.html'
    success_url = reverse_lazy('events:events')  # URL для редиректа после удаления (замени на правильное имя)
    slug_field = 'slug'
    slug_url_kwarg = 'event_slug'

    def test_func(self):
        event = self.get_object()  # Получаем объект события
        return (
            self.request.user == event.created_by or  # Проверяем автора события
            self.request.user.is_superuser or
            self.request.user.has_perm('events.delete_event')  # Правильное название permission для модели Event
        )
    
class EditEventPost(UpdateView):
    model = Event
    form_class = AddEditEventForm
    slug_field = "slug"               # ← поле в модели
    slug_url_kwarg = "event_slug"     # ← ключ из URL (в path)
    template_name = 'events/add_event.html'  # путь к шаблону для редактирования события
    success_url = reverse_lazy('events:events')  # редирект после успешного редактирования

    extra_context = {
        'title': "Редактирование мероприятия",
        'button':'Сохранить изменения'
    }

# Представление для фиксации подписки к мероприятию
class SubscribeCreateView(LoginRequiredMixin, CreateView):
    model = Subscribe
    fields = []  # Мы не показываем форму, просто создаём запись
    http_method_names = ['post']  # Только POST

    def form_valid(self, form):
        event = Event.objects.get(slug=self.kwargs['event_slug'])

        # Проверка на уже существующую подписку
        if Subscribe.objects.filter(user=self.request.user, event=event).exists():
            return redirect(reverse('events:event_detail', kwargs={'event_slug': event.slug}))

        form.instance.user = self.request.user
        form.instance.event = event
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('events:event_detail', kwargs={'event_slug': self.kwargs['event_slug']})
    
class UnsubscribeView(LoginRequiredMixin, View):
    def post(self, request, event_slug):
        event = get_object_or_404(Event, slug=event_slug)
        Subscribe.objects.filter(user=request.user, event=event).delete()
        return redirect(reverse('events:event_detail', kwargs={'event_slug': event_slug}))
    
