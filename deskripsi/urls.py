# deskripsi/urls.py

from django.urls import path
from .views import food_detail, food_detail_api

urlpatterns = [
    path('<int:food_id>/', food_detail, name='food_detail'),
    path('api/<int:food_id>/', food_detail_api, name='food_detail_api'),  # Tambahkan ini
]
