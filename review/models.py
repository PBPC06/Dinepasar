from django.db import models

class FoodReview(models.Model):
    food_name = models.CharField(max_length=100)
    rating = models.IntegerField()
    review_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.food_name} - {self.rating}/5"