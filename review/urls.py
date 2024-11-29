from django.urls import path
from . import views

app_name = 'review'

urlpatterns = [
    path('', views.show_main, name='forum'),
    path('add-review/', views.add_review, name='add_review'),
    path('edit/<int:review_id>/', views.edit_review, name='edit_review'),
    path('delete-review/<int:review_id>/', views.delete_review, name='delete_review'),
]
