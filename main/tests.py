from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from main.models import FoodEntry
from django.core.exceptions import ValidationError

class FoodEntryModelTest(TestCase):
    def setUp(self):
        self.food_entry = FoodEntry.objects.create(
            name="Test Food",
            description="Test description",
            price=50,
            rating=4
        )

    def test_food_entry_creation(self):
        """Test creating a FoodEntry object."""
        self.assertEqual(self.food_entry.name, "Test Food")
        self.assertEqual(self.food_entry.description, "Test description")
        self.assertEqual(self.food_entry.price, 50)
        self.assertEqual(self.food_entry.rating, 4)

    def test_food_entry_rating_validation(self):
        """Test rating validation within range 0 to 5."""
        with self.assertRaises(ValidationError):
            FoodEntry.objects.create(name="Invalid Rating", description="Test", price=50, rating=6).full_clean()

    def test_food_entry_price_validation(self):
        """Test that price cannot be negative."""
        with self.assertRaises(ValidationError):
            FoodEntry.objects.create(name="Negative Price", description="Test", price=-10, rating=3).full_clean()

class ShowMainViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
    
    def test_show_main_login_required(self):
        """Test that the show_main view redirects if user is not logged in."""
        response = self.client.get(reverse('main:show_main'))
        self.assertEqual(response.status_code, 302)  # Redirect to login page

    def test_show_main_logged_in(self):
        """Test that the show_main view loads for a logged-in user."""
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('main:show_main'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')
        # Check if last_login is in context
        self.assertIn('last_login', response.context)

class URLTests(TestCase):
    def test_show_main_url_resolves(self):
        """Test that the main page URL resolves correctly."""
        url = reverse('main:show_main')
        self.assertEqual(url, '/main/')  # Adjust if the path differs in your URLs config
