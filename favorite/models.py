from django.db import models
from django.contrib.auth.models import User
from search.models import Food
from django.conf import settings

# favorite/models.py
from django.conf import settings
from django.db import models

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Update this line
    food = models.ForeignKey(Food, on_delete=models.CASCADE)  # Assuming Food is defined in your models

    class Meta:
        unique_together = ('user', 'food')

    def __str__(self):
        return f"{self.user.username} - {self.food.nama_makanan}"

# Model untuk menyimpan informasi restoran favorit pengguna
class FavoriteRestaurant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relasi ke user
    name = models.CharField(max_length=255)  # Nama restoran
    address = models.CharField(max_length=255)  # Alamat restoran
    rating = models.DecimalField(max_digits=3, decimal_places=2)  # Rating restoran (misalnya 4.5)

    def __str__(self):
        return f"{self.name} - {self.user.username}"
