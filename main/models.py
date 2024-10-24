from django.db import models
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator

class FoodEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255) 
    description = models.TextField()
    price = models.IntegerField(validators=[MinValueValidator(0)]) 
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
