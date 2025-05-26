from django import forms
from .models import Event

class AddEditEventForm(forms.ModelForm):
    is_published = forms.BooleanField(
        required=False,
        initial=True,
        label="Опубликовать"
    )
    
    class Meta:
        model = Event
        fields = [
            'title', 'description', 'event_type', 
            'start_datetime', 'end_datetime', 'registration_deadline',
            'location', 'address', 'online_event', 'online_link',
            'organizer', 'contact_email', 'contact_phone', 'image',
            'is_published'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'start_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'registration_deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'online_link': forms.URLInput(attrs={'placeholder': 'https://example.com'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['start_datetime', 'end_datetime', 'registration_deadline']:
            field = self.fields.get(field_name)
            value = self.initial.get(field_name) or self.instance.__dict__.get(field_name)
            if value:
                # Преобразуем значение в нужный формат
                self.initial[field_name] = value.strftime('%Y-%m-%dT%H:%M')
