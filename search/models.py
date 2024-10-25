from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Food(models.Model):
    nama_makanan = models.CharField(max_length=255)
    restoran = models.CharField(max_length=255)
    kategori = models.CharField(max_length=100)
    gambar = models.TextField()
    deskripsi = models.TextField()
    harga = models.PositiveIntegerField()
    rating = models.FloatField()