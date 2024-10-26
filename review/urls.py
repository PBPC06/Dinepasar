from django.urls import path
from review.views import *

app_name = 'review'

urlpatterns = [
    path('', show_main, name='forum'),
    path('choose-food-review/', choose_food_review, name="choose_food_review"),
    path('add-review/', add_review, name="add_review"),
    # path('get-food-review/', get_food_review, name="get_food_review"),
    # path('get-food-review/<int:id>', get_food_review_by_id, name="get_food_review_by_id"),
    path('json/', show_json, name="show_json"),
    path('get-latest-reviews/', get_latest_reviews, name="get_latest_reviews"),
]