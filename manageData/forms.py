from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class NewUserForm(UserCreationForm):
    referral_code = forms.CharField(max_length=10, required=False)
    isAdmin = forms.ChoiceField(choices=[(True, "Admin"), (False, "User")], label="Admin/User", required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'referral_code', 'isAdmin')

    def clean(self):
        cleaned_data = super().clean()
        referral_code = cleaned_data.get('referral_code')
        is_admin = cleaned_data.get('isAdmin') == 'True'  # Konversi pilihan ke boolean

        # Validasi untuk pengguna dengan peran "Admin"
        if is_admin:
            if not referral_code:
                self.add_error('referral_code', "Referral code is required for Admin registration.")
            elif referral_code != "PBPC06WOW!":
                self.add_error('referral_code', "Invalid referral code. Please enter a valid code to register as an admin.")

        # Validasi untuk pengguna dengan peran "User"
        if not is_admin and referral_code:
            self.add_error('referral_code', "Referral code should only be filled if registering as Admin.")

        return cleaned_data
