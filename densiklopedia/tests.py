from django.test import TestCase, Client
from django.urls import reverse
from .models import ArticleEntry
from django.contrib.auth import get_user_model
from datetime import datetime
from django.http import JsonResponse, HttpResponse

User = get_user_model()

class DensiklopediaTests(TestCase):
    def setUp(self):
        # Create user for testing
        self.user = User.objects.create_user(username="testuser", password="password")
        self.other_user = User.objects.create_user(username="otheruser", password="password123")
        # Initialize client and login
        self.client = Client()
        self.client.login(username="testuser", password="password")
        
        # Create an article for testing
        self.article = ArticleEntry.objects.create(
            user=self.user,
            judul="Judul Artikel",
            gambar="https://example.com/image.jpg",
            subjudul="Subjudul Artikel",
            konten="Isi konten artikel.",
            waktu=datetime.now()
        )

    def test_show_json(self):
        response = self.client.get(reverse("densiklopedia:show_json"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertIsInstance(response, JsonResponse)
        # Verify JSON content includes expected data
        json_data = response.json()
        self.assertGreaterEqual(len(json_data), 1)

    def test_show_xml(self):
        response = self.client.get(reverse("densiklopedia:show_xml"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/xml")
        self.assertIsInstance(response, HttpResponse)

    def test_view_artikel(self):
        response = self.client.get(reverse("densiklopedia:view_artikel", args=[self.article.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Judul Artikel")
        self.assertContains(response, "Isi konten artikel.")

    def test_add_artikel_post(self):
        data = {
            "judul": "Artikel Baru",
            "gambar": "https://example.com/new_image.jpg",
            "subjudul": "Subjudul Baru",
            "konten": "Konten artikel baru."
        }
        response = self.client.post(reverse("densiklopedia:add_artikel"), data)
        self.assertEqual(response.status_code, 302)  # Status code after redirect
        self.assertTrue(ArticleEntry.objects.filter(judul="Artikel Baru").exists())

    def test_add_artikel_invalid_data(self):
        data = {
            "judul": "",
            "gambar": "not_a_url",
            "subjudul": "Subjudul Baru",
            "konten": ""
        }
        response = self.client.post(reverse("densiklopedia:add_artikel"), data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'judul', 'This field is required.')
        self.assertFormError(response, 'form', 'konten', 'This field is required.')

    def test_edit_artikel(self):
        data = {
            "judul": "Judul Artikel Edit",
            "gambar": "https://example.com/edited_image.jpg",
            "subjudul": "Subjudul Edit",
            "konten": "Konten artikel yang diedit."
        }
        response = self.client.post(reverse("densiklopedia:edit_artikel", args=[self.article.id]), data)
        self.assertEqual(response.status_code, 302)  # Status code after redirect
        self.article.refresh_from_db()
        self.assertEqual(self.article.judul, "Judul Artikel Edit")

    def test_edit_artikel_no_permission(self):
        # Test editing without permission
        self.client.logout()
        self.client.login(username="otheruser", password="password123")
        data = {
            "judul": "Unauthorized Edit",
            "gambar": "https://example.com/unauthorized_image.jpg",
            "subjudul": "Unauthorized",
            "konten": "This edit should not work."
        }
        response = self.client.post(reverse("densiklopedia:edit_artikel", args=[self.article.id]), data)
        self.assertEqual(response.status_code, 403)
        self.article.refresh_from_db()
        self.assertNotEqual(self.article.judul, "Unauthorized Edit")

    def test_delete_artikel(self):
        response = self.client.post(reverse("densiklopedia:delete_artikel", args=[self.article.id]))
        self.assertEqual(response.status_code, 302)  # Status code after redirect
        self.assertFalse(ArticleEntry.objects.filter(id=self.article.id).exists())

    def test_delete_artikel_no_permission(self):
        # Test deletion without permission
        self.client.logout()
        self.client.login(username="otheruser", password="password123")
        response = self.client.post(reverse("densiklopedia:delete_artikel", args=[self.article.id]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(ArticleEntry.objects.filter(id=self.article.id).exists())