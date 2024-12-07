# editProfile/urls.py
from django.urls import path
from .views import edit_profile, edit_profile_ajax, remove_food_from_history
from search.views import mark_food_as_tried

app_name = 'editProfile'

urlpatterns = [
    path('edit/', edit_profile, name='editProfile'),
    path('edit-ajax/', edit_profile_ajax, name='editProfileAjax'),    
    path('mark_food_as_tried/<int:food_id>/', mark_food_as_tried, name='mark_food_as_tried'),
    path('remove_food_from_history/<int:food_id>/', remove_food_from_history, name='remove_food_from_history'),

]