from django.db import models
from manageData.models import CustomUser
from search.models import Food  # Import Food model

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    about_me = models.TextField(blank=True, null=True)
    # New field to store user's tried foods
    tried_foods = models.ManyToManyField(Food, blank=True)

    def __str__(self):
        return self.user.username
