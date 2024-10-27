# deskripsi/urls.py

from django.urls import path
from .views import food_detail

urlpatterns = [
    path('<int:food_id>/', food_detail, name='food_detail'),
]
