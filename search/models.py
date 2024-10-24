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

class CustomUser(AbstractUser):
    OWNER = 'owner'
    USER = 'user'
    
    ROLE_CHOICES = [
        (OWNER, 'Owner'),
        (USER, 'User'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=USER)

        # Tambahkan related_name di sini untuk menghindari konflik dengan auth.User
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Custom related name
        blank=True,
        help_text='The groups this user belongs to.'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Custom related name
        blank=True,
        help_text='Specific permissions for this user.'
    )