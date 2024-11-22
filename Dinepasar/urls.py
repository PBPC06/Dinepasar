"""
URL configuration for Dinepasar project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from manageData.views import login_user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('manageData/', include('manageData.urls')),
    path('editProfile/', include('editProfile.urls')),
    path('login/', login_user, name='login'),
    path('search/', include('search.urls')),
    path('deskripsi/', include('deskripsi.urls')),
    path('favorite/', include('favorite.urls', namespace='favorite')),
    path('densiklopedia/', include('densiklopedia.urls')),
    path('review/', include('review.urls')),
]
