from django import forms
from .models import RecurringBusyTime

class RecurringBusyTimeForm(forms.ModelForm):
    class Meta:
        model = RecurringBusyTime
        fields = ['day_of_week', 'start_time', 'end_time', 'description']
        widgets = {
            'day_of_week': forms.Select(attrs={'class': 'form-select'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }