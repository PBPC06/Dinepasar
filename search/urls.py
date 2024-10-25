from django.urls import path
from . import views
from search.views import get_foods, login_user, register, logout_user, edit_food, delete_food, add_food
app_name = "search"

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('food/add/', add_food, name='add_food'),
    path('owner/dashboard/', views.owner_dashboard, name='owner_dashboard'),
    path('food/<int:food_id>/edit/', edit_food, name='edit_food'),
    path('food/<int:food_id>/delete/', delete_food, name='delete_food'),
    path("api/foods/", get_foods, name="get_foods"),  # Mengakses data JSON
    path('search/', views.food_search, name='food_search'),  # Mengakses halaman search

]