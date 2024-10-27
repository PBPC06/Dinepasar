# favorite/urls.py

from django.urls import path
from .views import add_to_favorite, favorite_list, delete_favorite
from . import views

app_name = 'favorite'

urlpatterns = [
    path('add/', add_to_favorite, name='add_to_favorite'),
    path('', favorite_list, name='favorite_list'),
    path('delete_favorite/<int:favorite_id>/', views.delete_favorite, name='delete_favorite'),  # URL for deleting favorite
]
