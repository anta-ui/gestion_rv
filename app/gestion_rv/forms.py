from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'time', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.TextInput(attrs={'type':'text'})
            
        }
        labels = {
            'date': 'Date du rendez-vous',
            'time': 'Heure du rendez-vous',
            'description': 'Description',
        }
