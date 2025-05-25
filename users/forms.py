from cProfile import label
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.forms import widgets
from django.utils.translation import gettext_lazy as _
User = get_user_model()


#Регистрация
class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"})
    )
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        labels = {
            'email': 'E-mail',
            'first_name': "Имя",
            'last_name': "Фамилия",
        }
    widgets = {
            'email': forms.TextInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }
# Профиль
class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.CharField(disabled=True, label='E-mail', widget=forms.TextInput(attrs={'class': 'form-input'}))
    class Meta: 
        model = get_user_model() 
        fields = ['username', 'email', 'first_name', 'last_name', 'photo']
        labels = { 'first_name': 'Имя', 'Last_name': 'Фамилия',} 
        widgets = { 
            'first_name': forms.TextInput(attrs={'class': 'form-input'}), 
            'Last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }
#Логин
class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Логин",
                    widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label="Пароль",
                    widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']
 

 # class UserCreationForm(UserCreationForm):
#     email = forms.EmailField(
#         label=_("Email"),
#         max_length=254,
#         widget=forms.EmailInput(attrs={"autocomplete": "email"})
#     )
#     class Meta(UserCreationForm.Meta):
#         model = get_user_model()
#         fields = ("username","email") 