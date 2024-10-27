from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Favorite
from search.models import Food
from django.contrib.auth import get_user_model

User = get_user_model()

class FavoriteTests(TestCase):
    def setUp(self):
        # Create a user and food item for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.food = Food.objects.create(
            nama_makanan='Burger',
            deskripsi='Juicy grilled burger',
            restoran='http://restaurant.com',
            rating=4.0,
            harga=30000,
            gambar='http://image.com/burger.jpg',
            kategori='Fast Food'
        )
        self.client.login(username='testuser', password='testpassword')

    def test_add_to_favorite(self):
        # Add food to favorites
        response = self.client.post(reverse('favorite:add_to_favorite'), {'food_id': self.food.id})
        self.assertEqual(response.status_code, 201)
        self.assertJSONEqual(response.content, {'message': 'Food added to favorites!'})
        self.assertEqual(Favorite.objects.count(), 1)

    def test_add_duplicate_favorite(self):
        # Add the same food to favorites twice
        Favorite.objects.create(user=self.user, food=self.food)
        response = self.client.post(reverse('favorite:add_to_favorite'), {'food_id': self.food.id})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'message': 'This item is already in your favorites.'})
        self.assertEqual(Favorite.objects.count(), 1)

    def test_add_to_favorite_invalid_food(self):
        # Try to add a non-existent food to favorites
        response = self.client.post(reverse('favorite:add_to_favorite'), {'food_id': 9999})
        self.assertEqual(response.status_code, 404)

    def test_favorite_list_view(self):
        # View the favorite list page
        Favorite.objects.create(user=self.user, food=self.food)
        response = self.client.get(reverse('favorite:favorite_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.food.nama_makanan)
        self.assertTemplateUsed(response, 'favorite/favorite_list.html')

    def test_delete_favorite(self):
        # Delete a favorite food item
        favorite = Favorite.objects.create(user=self.user, food=self.food)
        response = self.client.post(reverse('favorite:delete_favorite', args=[favorite.id]))
        self.assertEqual(response.status_code, 302)  # Redirects after deletion
        self.assertEqual(Favorite.objects.count(), 0)
