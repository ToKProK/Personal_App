from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView
from users.forms import ProfileUserForm, UserCreationForm
from django.shortcuts import render
from django.contrib.auth import authenticate, get_user, get_user_model
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin

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


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': "Профиль пользователя"}

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user
