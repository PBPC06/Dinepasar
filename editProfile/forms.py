# editProfile/forms.py
from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'email', 'about_me']
        widgets = {
            'about_me': forms.Textarea(attrs={'rows': 4}),
        }
