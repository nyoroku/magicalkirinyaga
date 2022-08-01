from .models import Application, Latest
from django import forms


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('firstname', 'lastname', 'phone', 'email', 'qualification', 'course', 'aboutus',)
        exclude = ('applied',)


class EventForm(forms.ModelForm):
    class Meta:
        model = Latest
        fields = ('title', 'day', 'start', 'end', 'detail', 'location', 'photo')

