from django.views import View
from users.forms import UserCreationForm
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.shortcuts import redirect

# Create your views here.
class Register(View):
    template_name = 'registration/register.html'
    def get(self, request):
        context = { 
            'form': UserCreationForm() 
        }
        return render(request, self.template_name, context)
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
        context = {
            'form' : form
        }
        return render(request, self.template_name, context)

def user_account(request): # Страница с аккаунтом
    return render(request, 'users/account.html')