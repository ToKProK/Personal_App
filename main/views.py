from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render 

# Create your views here.
def index(request):
    return render(request, 'main/home.html')
@login_required #Запрещает заходит не зарегестрированным пользователям
def about(request):
    return HttpResponse('About Page')
