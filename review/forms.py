from django.forms import ModelForm
from .models import FoodReview

class ReviewFoodForm(ModelForm):
    class Meta:
        model = FoodReview
        fields = ["rating", "review_message"]