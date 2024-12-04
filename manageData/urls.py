from django.urls import path
from manageData.views import register, login_user, logout_user, login_flutter, register_flutter

app_name = 'manageData'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('login_flutter/', login_flutter, name='login_flutter'),
    path('register_flutter/', register_flutter, name='register_flutter'),
]