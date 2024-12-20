from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Food(models.Model):
    nama_makanan = models.CharField(max_length=255)
    kategori = models.CharField(max_length=100)
    gambar = models.URLField(max_length=500, blank=True, null=True)
    deskripsi = models.TextField(blank=True, null=True)  # Tambahkan field ini
    restoran = models.CharField(max_length=255, blank=True, null=True)  # Tambahkan field ini
    harga = models.IntegerField()
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.nama_makanan
