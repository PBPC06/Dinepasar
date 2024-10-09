from django.db import models
import uuid 

class FoodEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # mood = models.CharField(max_length=255)
    # time = models.DateField(auto_now_add=True)
    # feelings = models.TextField()
    # mood_intensity = models.IntegerField()

    # @property
    # def is_mood_strong(self):
    #     return self.mood_intensity > 5
