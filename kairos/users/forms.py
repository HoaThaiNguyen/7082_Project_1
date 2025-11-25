from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname', 'bio', 'profile_picture', 'is_calendar_public']
        widgets = {
            'is_calendar_public': forms.CheckboxInput(attrs={'class': 'toggle-checkbox'}),
            'bio': forms.Textarea(attrs={
                'class': 'form-textarea rounded border px-3 py-2',
                'rows': 3,
                'placeholder': 'Write something about yourself'
            }),
        }
