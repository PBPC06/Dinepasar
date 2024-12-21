from django.urls import path
from . import views

app_name = 'review'

urlpatterns = [
    path('', views.show_main, name='forum'),
    path('add-review/', views.add_review, name='add_review'),
    path('add-review-flutter/', views.add_review_flutter, name='add_review_flutter'),
    path('edit/<int:review_id>/', views.edit_review, name='edit_review'),
    path('delete-review/<int:review_id>/', views.delete_review, name='delete_review'),
    path('json/', views.show_json, name='show_json'),
    path('json_all/', views.show_json_all, name='show_json_all'),
    path('json/user/<str:username>/', views.show_json_by_user, name='show_json_by_user'),  # Endpoint untuk ulasan berdasarkan username

]
