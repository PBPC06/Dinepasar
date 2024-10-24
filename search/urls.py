from django.urls import path
from . import views
from search.views import get_foods
app_name = "search"

urlpatterns = [
    path("api/foods/", get_foods, name="get_foods"),  # Mengakses data JSON
    path('', views.food_search, name='food_search'),  # Mengakses halaman search
    path('admin/edit/<int:pk>/', views.edit_food, name='edit_food'),
    path('admin/delete/<int:pk>/', views.delete_food, name='delete_food'),
    path('<int:pk>/', views.food_preview, name='food_preview'),  # Untuk halaman detail
]