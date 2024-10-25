from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class NewUserForm(UserCreationForm):
    referral_code = forms.CharField(max_length=10, required=False)
    isAdmin = forms.ChoiceField(choices=[(True, "Admin"), (False, "User")], label="Admin/User", required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'referral_code')

    def clean(self):
        cleaned_data = super().clean()
        referral_code = cleaned_data.get('referral_code')
        is_admin = cleaned_data.get('isAdmin')

        # Validate the referral code
        if referral_code != "PBPC06WOW!" and is_admin:
            self.add_error('referral_code', "Invalid referral code. Please enter a valid code to register as an admin.")
            cleaned_data['isAdmin'] = False  # Reset to default user role if code is incorrect

        return cleaned_data
