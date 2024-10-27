import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# from main.models import FoodEntry
from manageData.models import CustomUser

@login_required(login_url='/login')
def show_main(request):
    user = request.user
    last_login = request.COOKIES.get('last_login')

    context = {
        'last_login': last_login,
    }
    return render(request, 'main.html', context)
