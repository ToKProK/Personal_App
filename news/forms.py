from turtle import title
from django import forms
from django.forms import widgets

from news.models import News 

# class AddNewsForm(forms.Form): # Метод не связанный с django моделями
#     title = forms.CharField(max_length=255, label="Название")
#     content = forms.CharField(widget=forms.Textarea(), required=False, label="Описание")
#     is_published = forms.BooleanField(required=False, label="Опубликовать", initial=True)
#     # 46
class AddNewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'photo', 'is_published']
        widgets = {
            'title' : forms.TextInput(attrs={'class':'form-input'}),
            'content': forms.Textarea(),
            "is_published": forms.CheckboxInput()
         } 