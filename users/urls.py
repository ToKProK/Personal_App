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
import profile
from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView
app_name = "users"

urlpatterns = [
    # path('users /register/', views.Register.as_view(), name='register'),
    path('profile/', views.ProfileUser.as_view(), name='profile'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("register/",  views.RegisterUser.as_view(), name="register"),
    path('', include('django.contrib.auth.urls')),
]
