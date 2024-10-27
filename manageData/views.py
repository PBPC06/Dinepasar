import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages
from main.forms import FoodEntryForm
from main.models import FoodEntry
from django.views.decorators.csrf import csrf_exempt
from .forms import NewUserForm
from django.http import JsonResponse
from django.contrib.auth.models import User

@csrf_exempt
@csrf_exempt
def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Save form tapi belum masuk ke database

            if form.cleaned_data.get('isAdmin') == "Admin":
                user.is_admin = True
            else:
                user.is_admin = False
            
            user.save() # Save ke database
            
            messages.success(request, 'Your account has been successfully created!')
            return redirect('manageData:login')
    else:
        form = NewUserForm()

    context = {'form': form}
    return render(request, 'register.html', context)

@csrf_exempt
def login_user(request):
    

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response

    else:
      form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'login.html', context)

def logout_user(request):


    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

