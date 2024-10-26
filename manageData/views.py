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
def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        
        # Check if the form is valid
        if form.is_valid():
            user = form.save(commit=False)  # Save the form without committing to the database yet
            
            # Set the is_admin field based on the form selection
            user.is_admin = form.cleaned_data.get('isAdmin') == 'True'  # Ensure correct boolean assignment
            
            user.save()  # Now save the user to the database
            
            messages.success(request, 'Your account has been successfully created!')
            return redirect('manageData:login')
        # else:
        #     # If the form is not valid, add error messages to the request
        #     for field, errors in form.errors.items():
        #         for error in errors:
        #             messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = NewUserForm()  # Initialize form when method is GET

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
            # Menambahkan pesan kesalahan jika form tidak valid
            messages.error(request, "Invalid username or password. Please try again.")

    else:
        form = AuthenticationForm()

    context = {'form': form}
    return render(request, 'login.html', context)

def logout_user(request):


    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

