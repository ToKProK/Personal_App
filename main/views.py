from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render 
from main.forms import UploadFileForm
# Create your views here.
def index(request):
    return render(request, 'main/home.html')



@login_required #Запрещает заходит не зарегестрированным пользователям
def about(request):
    if request.method == 'POST': # Если: получаем POST запрос / загружается изображение
        #handle_uploaded_file(request.FILES['file_upload']) # "file_upload" Такое название присвоенной в html странице
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(form.cleaned_data['file'])# "file" название атрибута класса "UploadFileForm"
    else:
        form = UploadFileForm()
    return render(request, 'main/about.html', {'form' : form,})

def handle_uploaded_file(f): # 48
    with open(f"main/images_about/{f.name}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)