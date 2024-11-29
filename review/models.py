from django.db import models
from django.conf import settings
from search.models import Food

class FoodReview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    rating = models.FloatField()
    review_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)