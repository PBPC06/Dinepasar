from django.test import TestCase
from django.urls import reverse
from manageData.models import CustomUser
from search.models import Food

class FoodDetailViewTests(TestCase):
    def setUp(self):
        # Create a user and a food item for testing
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.food = Food.objects.create(
            nama_makanan='Pizza',
            deskripsi='Delicious Italian pizza',
            restoran='http://restaurant.com',
            rating=4.5,
            harga=50000,
            gambar='http://image.com/pizza.jpg',
            kategori='Italian'
        )

    def test_food_detail_view(self):
        # Access the food detail view
        response = self.client.get(reverse('food_detail', args=[self.food.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.food.nama_makanan)
        self.assertTemplateUsed(response, 'deskripsi/detail.html')

    def test_food_detail_view_nonexistent_food(self):
        # Try to access a non-existent food item
        response = self.client.get(reverse('food_detail', args=[9999]))
        self.assertEqual(response.status_code, 404)
