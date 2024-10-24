from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class NewUserForm(UserCreationForm):
    referral_code = forms.CharField(max_length=10, required=False)
    isAdmin = forms.ChoiceField(choices=[(True, "Admin"), (False, "User")], label="Admin/User", required=False)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'referral_code')

    def clean(self):
        cleaned_data = super().clean()
        referral_code = cleaned_data.get('referral_code')
        is_admin = cleaned_data.get('isAdmin')
        
        # Check if the referral code matches for admin role
        if referral_code == "PBPC06WOW!":
            cleaned_data['isAdmin'] = True  # Assign admin role
        else:
            cleaned_data['isAdmin'] = False  # Default to user if code doesn't match
        
        return cleaned_data
