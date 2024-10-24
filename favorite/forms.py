from django import forms
from .models import FavoriteRestaurant

class FavoriteRestaurantForm(forms.ModelForm):
    class Meta:
        model = FavoriteRestaurant
        fields = ['name']  # Pastikan hanya mencantumkan field yang ada di model
