from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname', 'bio', 'profile_picture', 'is_calendar_public']
        widgets = {
            'nickname': forms.TextInput(attrs={
                'class': 'border',
            }),

            'bio': forms.Textarea(attrs={
                'class': 'border px-3 py-3 w-full',
                'rows': 3,
                'placeholder': 'Write something about yourself'
            }),

            'profile_picture': forms.FileInput(attrs={
                'class': 'border',
            }),

            'is_calendar_public': forms.CheckboxInput(attrs={
                'class': 'toggle-checkbox'
            }),   
        }
