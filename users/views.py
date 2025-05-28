from telnetlib import AUTHENTICATION
from turtle import title
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView
from users.forms import ProfileUserForm, UserCreationForm
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, get_user, get_user_model
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LoginUserForm, RegisterUserForm, UserPasswordChangeForm


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = "registration/login.html"
    extra_context ={"title":"Авторизация"}

#LoginRequiredMixin - не позволяет зати не зарегестрированному пользователю
#Открывает окно регистрации пользователя
class RegisterUser(LoginRequiredMixin,CreateView):
    form_class = RegisterUserForm
    template_name = "registration/register.html"
    extra_context = {"title":"Регистрация"}
    success_url = reverse_lazy("users:login")



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