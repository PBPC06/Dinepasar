from django.urls import path
from . import views

app_name = 'review'

urlpatterns = [
    path('', views.show_main, name='forum'),
    path('choose-food/', views.choose_food, name='choose_food'),
    path('add-review/', views.add_review, name='add_review'),
    path('json/', views.show_json, name='show_json'),
    path('get-latest-reviews/', views.get_latest_reviews, name='get_latest_reviews'),
]
