from django.urls import path
from manageData.views import register, login_user, logout_user
# from . import views

app_name = 'manageData'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    # path('json/', views.food_entries_json, name='food_entries_json'),
]