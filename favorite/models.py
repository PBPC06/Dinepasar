from django.db import models
from django.contrib.auth.models import User

# Model untuk menyimpan informasi restoran favorit pengguna
class FavoriteRestaurant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relasi ke user
    name = models.CharField(max_length=255)  # Nama restoran
    address = models.CharField(max_length=255)  # Alamat restoran
    rating = models.DecimalField(max_digits=3, decimal_places=2)  # Rating restoran (misalnya 4.5)

    def __str__(self):
        return f"{self.name} - {self.user.username}"
