from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings
from .views import add_to_favorite, favorite_list, delete_favorite

app_name = 'favorite'

urlpatterns = [
    path('add/', add_to_favorite, name='add_to_favorite'),
    path('', favorite_list, name='favorite_list'),
    path('delete_favorite/<int:favorite_id>/', delete_favorite, name='delete_favorite'),  # URL for deleting favorite
]
