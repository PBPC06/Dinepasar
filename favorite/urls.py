# favorite/urls.py

from django.urls import path
from .views import add_to_favorite, favorite_list

app_name = 'favorite'

urlpatterns = [
    path('add/', add_to_favorite, name='add_to_favorite'),
    path('', favorite_list, name='favorite_list'),
]
