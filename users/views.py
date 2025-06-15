from telnetlib import AUTHENTICATION
from turtle import title
from django import forms
from django.core.mail import send_mail
from django.db.models import Q
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from Personal_App import settings
from users.forms import ProfileUserForm, UserCreationForm
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, get_user, get_user_model
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LoginUserForm, RegisterUserForm, UserPasswordChangeForm
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import UserPassesTestMixin

User = get_user_model()  # Используем текущую модель пользователя

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = "registration/login.html"
    extra_context ={"title":"Авторизация"}

#LoginRequiredMixin - не позволяет зати не зарегестрированному пользователю
#Открывает окно регистрации пользователя
class RegisterUser(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    form_class = RegisterUserForm
    template_name = "registration/register.html"
    extra_context = {"title":"Регистрация"}
    success_url = reverse_lazy("users:register")
    def form_valid(self, form):
        user = form.save(commit=False)
        password = form.cleaned_data.get('password1')  # или как у тебя называется поле пароля
        user.set_password(password)
        user.save()

        # Отправляем письмо
        current_site = get_current_site(self.request)
        site_url = f"http://{current_site.domain}"

        subject='Добро пожаловать в Весь Мир Един',
        message = (
            f"Здравствуйте, {user.username}!\n\n"
            f"Ваш логин: {user.username}\n"
            f"Ваш пароль: {password}\n\n"
            f"Перейдите по ссылке для входа: {site_url}/login/\n\n"
            "Спасибо за регистрацию!"
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        messages.success(self.request, f"Пользователь {user.username} успешно зарегистрирован(а)!")
        return super().form_valid(form)
    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.is_staff or user.groups.filter(name='Руководитель').exists()

# ОТкрывает профиль зарегестрированного пользователя
class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': "Профиль пользователя"}

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user
    


class UserListView(LoginRequiredMixin,UserPassesTestMixin,ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset().order_by('username')
        query = self.request.GET.get('q')
        group = self.request.GET.get('group')

        if query:
            queryset = queryset.filter(
                Q(username__icontains=query) |
                Q(email__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            )

        if group:
            queryset = queryset.filter(groups__name=group)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')  # Чтобы совпадало с шаблоном
        context['groups'] = Group.objects.all()
        context['selected_group'] = self.request.GET.get('group', '')
        return context
    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.is_staff or user.groups.filter(name='Руководитель').exists()
    
# class UserDetailView(DetailView):
#     model = User
#     template_name = 'users/user_detail.html'  # Создай такой шаблон
#     context_object_name = 'user_obj'  # Чтобы в шаблоне обращаться как user_obj

class UserAdminUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = User
    template_name = 'users/user_detail.html'
    context_object_name = 'user_obj'
    fields = ['username', 'email', 'first_name', 'last_name', 'groups']  # groups работает только если User имеет ManyToMany к Group
    success_url = reverse_lazy('users:users_list')  # куда редирект после сохранения (замени на нужный URL)

    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.is_staff or user.groups.filter(name='Руководитель').exists()

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        # Отключаем возможность редактировать определённые поля
        readonly_fields = ['username', 'first_name', 'last_name']
        for field in readonly_fields:
            form.fields[field].disabled = True
            form.fields[field].widget.attrs.update({'class': 'form-control readonly-field'})

 # Сделать поле groups множественным выбором с виджетом SelectMultiple
        form.fields['groups'] = forms.ModelMultipleChoiceField(
            queryset=Group.objects.all(),
            required=False,
            label="Группы пользователя",
            widget=forms.SelectMultiple(attrs={'class': 'form-control'})
        )

        # Установить начальные выбранные группы текущего пользователя
        form.initial['groups'] = self.get_object().groups.all()

        return form


    def post(self, request, *args, **kwargs):
        if "delete_user" in request.POST:
            self.object = self.get_object()
            self.object.delete()
            return redirect('users:users_list')  # редирект после удаления
        return super().post(request, *args, **kwargs)

class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'  # Создай этот шаблон
    success_url = reverse_lazy('users:users_list')  # Перенаправление после удаления
    
    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.is_staff or user.groups.filter(name='Руководитель').exists()
    