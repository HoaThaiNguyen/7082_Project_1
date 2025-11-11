from django import forms
from .models import BusyTime

class BusyTimeForm(forms.ModelForm):
    class Meta:
        model = BusyTime
        fields = ['day_of_week', 'start_time', 'end_time', 'description']
