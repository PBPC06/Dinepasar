from django.test import TestCase, Client
from django.urls import reverse
from .models import Food
from .forms import FoodForm
from django.http import JsonResponse
import json
from django.contrib.auth import get_user_model
from unittest.mock import patch


User = get_user_model()  # Get the custom user model

class FoodModelTest(TestCase):
    def setUp(self):
        Food.objects.all().delete()  # Clear out existing food objects
        self.food = Food.objects.create(
            nama_makanan="Nasi Goreng",
            restoran="Warung Ibu",
            kategori="Makanan",
            gambar="image_url",
            deskripsi="Nasi goreng enak",
            harga=20000,
            rating=4.5
    )

    def test_food_creation(self):
        """Test if a Food instance is created successfully"""
        self.assertEqual(Food.objects.count(), 1)

    def test_food_str_method(self):
        """Test the __str__ method of Food model"""
        self.assertEqual(str(self.food), self.food.nama_makanan)


class FoodFormTest(TestCase):
    def test_food_form_valid_data(self):
        """Test FoodForm with valid data"""
        form_data = {
            'nama_makanan': 'Mie Goreng',
            'restoran': 'Warung Budi',
            'kategori': 'Makanan',
            'gambar': 'image_url',
            'deskripsi': 'Mie goreng enak',
            'harga': 18000,
            'rating': 4.0
        }
        form = FoodForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_food_form_invalid_data(self):
        form_data = {
            'nama_makanan': '',
            'harga': -1,  # Invalid price
            # Omitting 'rating' to focus on required fields
        }
        form = FoodForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('nama_makanan', form.errors)
        self.assertIn('harga', form.errors)


class FoodViewsTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')  # Log in the user

        # Create a food item for testing
        self.food = Food.objects.create(
            nama_makanan='Nasi Goreng',
            restoran='Restoran A',
            kategori='Main Course',
            gambar='http://example.com/image.jpg',
            deskripsi='Delicious fried rice.',
            harga=60000,
            rating='5'
        )

    def test_get_foods(self):
        response = self.client.get(reverse('search:get_foods'))
        self.assertEqual(response.status_code, 200)

    def test_food_search(self):
        response = self.client.post(reverse('search:food_search'), {'keyword': 'Nasi'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nasi Goreng')

    def test_owner_dashboard(self):
        response = self.client.post(reverse('search:owner_dashboard'), {'keyword': 'Nasi'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nasi Goreng')

    def test_add_food(self):
        response = self.client.post(reverse('search:add_food'), {
            'nama_makanan': 'Sate',
            'restoran': 'Restoran B',
            'kategori': 'Snack',
            'gambar': 'http://example.com/sate.jpg',
            'deskripsi': 'Grilled meat skewers.',
            'harga': '45000',
            'rating': '4'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Food.objects.filter(nama_makanan='Sate').exists())

    def test_edit_food(self):
        response = self.client.post(reverse('search:edit_food', kwargs={'food_id': self.food.id}), {
            'nama_makanan': 'Nasi Goreng Special',
            'restoran': 'Restoran A',
            'kategori': 'Main Course',
            'gambar': 'http://example.com/image.jpg',
            'deskripsi': 'Special delicious fried rice.',
            'harga': '70000',
            'rating': '5'
        })
        self.assertEqual(response.status_code, 200)
        self.food.refresh_from_db()
        self.assertEqual(self.food.nama_makanan, 'Nasi Goreng Special')

    def test_delete_food(self):
        response = self.client.delete(reverse('search:delete_food', kwargs={'food_id': self.food.id}))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Food.objects.filter(id=self.food.id).exists())

    def test_search_redirect_authenticated_admin(self):
        # Assuming there's a way to set the user as an admin
        self.user.is_admin = True
        self.user.save()
        response = self.client.get(reverse('search:search_redirect'))
        self.assertRedirects(response, reverse('search:owner_dashboard'))

    def test_fetch_foods(self):
        response = self.client.get(reverse('search:fetch_foods'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nasi Goreng')

class EditFoodViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='password', is_admin=True)
        self.food = Food.objects.create(
            gambar='http://example.com/image.jpg',
            nama_makanan='Nasi Goreng',
            restoran='Restoran A',
            kategori='Makanan Utama',
            harga=50000,
            rating=4.5,
            deskripsi='Deskripsi Nasi Goreng'
        )
        self.client.login(username='admin', password='password')

    def test_edit_food_view_status_code(self):
        response = self.client.get(reverse('search:edit_food', args=[self.food.id]))
        self.assertEqual(response.status_code, 200)

    def test_edit_food_template_used(self):
        response = self.client.get(reverse('search:edit_food', args=[self.food.id]))
        self.assertTemplateUsed(response, 'edit_foods.html')

    @patch('search.views.edit_food')
    def test_edit_food_failure(self, mock_edit_food):
        mock_edit_food.return_value = json.dumps({
            'errors': {
                'nama_makanan': ['This field is required.'],
                'harga': ['Ensure this value is greater than or equal to 0.']
            }
        })
        response = self.client.post(reverse('search:edit_food', args=[self.food.id]), {
            'gambar': '',
            'nama_makanan': '',
            'restoran': 'Restoran B',
            'kategori': 'Makanan Utama',
            'harga': -5000,  # Invalid
            'rating': 5,
            'deskripsi': 'Deskripsi Nasi Goreng Spesial'
        }, content_type='application/json')

        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertIn('errors', response_data)
        self.assertIn('nama_makanan', response_data['errors'])
