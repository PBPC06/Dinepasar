from django.urls import path
from . import views
from search.views import get_foods,  edit_food, delete_food, add_food, fetch_foods
app_name = "search"

urlpatterns = [
    path('search/', views.search_redirect, name='search_redirect'),
    path('food/add/', add_food, name='add_food'),
    path('owner/dashboard/', views.owner_dashboard, name='owner_dashboard'),
    path('food/<int:food_id>/edit/', edit_food, name='edit_food'),
    path('delete/<int:food_id>/', delete_food, name='delete_food'),
    path("api/foods/", get_foods, name="get_foods"),  # Mengakses data JSON
    path('food-search/', views.food_search, name='food_search'),  # Mengakses halaman search
    path('<int:pk>/', views.food_preview, name='food_preview'),  # Untuk halaman detail
    path('food/<int:pk>/', views.food_detail, name='food_detail'),
    path('fetch_foods/', fetch_foods, name='fetch_foods'),
]