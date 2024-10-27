# manageData/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .forms import NewUserForm
from .models import CustomUser

User = get_user_model()


class ManageDataTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('manageData:register')
        self.login_url = reverse('manageData:login')
        self.logout_url = reverse('manageData:logout')
        self.user_data = {
            "username": "testuser",
            "password1": "complexpassword123!",
            "password2": "complexpassword123!",
            "isAdmin": "False",
        }
        self.admin_data = {
            "username": "adminuser",
            "password1": "complexpassword123!",
            "password2": "complexpassword123!",
            "isAdmin": "True",
            "referral_code": "PBPC06WOW!"
        }

    def test_register_view_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_register_user_success(self):
        response = self.client.post(self.register_url, data=self.user_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="testuser").exists())
        self.assertRedirects(response, self.login_url)

    def test_register_admin_with_referral_code(self):
        response = self.client.post(self.register_url, data=self.admin_data)
        self.assertEqual(response.status_code, 302)
        admin_user = User.objects.get(username="adminuser")
        self.assertTrue(admin_user.is_admin)
        self.assertRedirects(response, self.login_url)

    def test_register_admin_invalid_referral_code(self):
        self.admin_data["referral_code"] = "WRONGCODE"
        response = self.client.post(self.register_url, data=self.admin_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, "form", "referral_code", "Invalid referral code. Please enter a valid code to register as an admin.")
        self.assertFalse(User.objects.filter(username="adminuser").exists())

    def test_login_user(self):
        User.objects.create_user(username="testuser", password="complexpassword123!")
        response = self.client.post(self.login_url, {"username": "testuser", "password": "complexpassword123!"})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main:show_main'))

    def test_login_invalid_credentials(self):
        response = self.client.post(self.login_url, {"username": "fakeuser", "password": "wrongpassword"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, "Please enter a correct username and password.")

    def test_logout_user(self):
        User.objects.create_user(username="testuser", password="complexpassword123!")
        self.client.login(username="testuser", password="complexpassword123!")
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)

    def test_new_user_form_valid(self):
        form = NewUserForm(data=self.user_data)
        self.assertTrue(form.is_valid())

    def test_new_user_form_admin_invalid_referral(self):
        form = NewUserForm(data={**self.admin_data, "referral_code": "WRONGCODE"})
        self.assertFalse(form.is_valid())
        self.assertIn("referral_code", form.errors)
