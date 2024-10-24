from django.urls import path
from . import views

urlpatterns = [
    path('favorites/', views.favorite_list, name='favorite_list'),
    path('favorites/remove/<int:restaurant_id>/', views.remove_favorite, name='remove_favorite'),
]
