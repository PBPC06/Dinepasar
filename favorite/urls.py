from django.urls import path
from .views import add_to_favorite, favorite_list, delete_favorite, get_csrf_token, get_recommended, favorite_list_api, delete_favorite_api

app_name = 'favorite'

urlpatterns = [
    path('add/', add_to_favorite, name='add_to_favorite'),
    path('', favorite_list, name='favorite_list'),
    path('delete_favorite/<int:favorite_id>/', delete_favorite, name='delete_favorite'),  # URL for deleting favorite
    path('get-csrf-token/', get_csrf_token, name='get_csrf_token'),
    path('recommended/', get_recommended, name='get_recommended'),
    path('api/', favorite_list_api, name='favorite_list_api'),
    path('delete/<int:favorite_id>/', delete_favorite_api, name='delete_favorite_api'),
]
