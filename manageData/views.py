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
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import CustomUser
User = get_user_model()

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


@csrf_exempt
def login_flutter(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            # Kirim informasi role user
            return JsonResponse({
                "username": user.username,
                "status": True,
                "is_admin": user.is_admin,  # Ambil nilai is_admin dari model CustomUser
                "message": "Login sukses!"
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Login gagal, akun dinonaktifkan."
            }, status=401)
    else:
        return JsonResponse({
            "status": False,
            "message": "Login gagal, periksa kembali username atau kata sandi."
        }, status=401)

@csrf_exempt
def logout_flutter(request):
    if request.method == 'POST':
        auth_logout(request)
        return JsonResponse({
            "status": True,
            "message": "Logout successful!"
        }, status=200)
    else:
        return JsonResponse({
            "status": False,
            "message": "Invalid request method."
        }, status=400)

@csrf_exempt
def register_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password1 = data['password1']
        password2 = data['password2']
        referral_code = data.get('referral_code', '')  # Ambil kode referal (bisa kosong)

        # Check if the passwords match
        if password1 != password2:
            return JsonResponse({
                "status": False,
                "message": "Passwords do not match."
            }, status=400)

        # Cek jika referral_code diberikan (hanya valid jika user mendaftar sebagai admin)
        if referral_code and referral_code != "PBPC06WOW!":
            return JsonResponse({
                "status": False,
                "message": "Invalid referral code."
            }, status=400)
        
        

        # Cek apakah username sudah ada
        if CustomUser.objects.filter(username=username).exists():
            return JsonResponse({
                "status": False,
                "message": "Username already exists."
            }, status=400)

        # Default: pengguna bukan admin
        is_admin = False

        # Jika referral code valid, set sebagai admin
        if referral_code == "PBPC06WOW!":
            is_admin = True

        # Buat pengguna baru
        user = CustomUser.objects.create_user(
            username=username,
            password=password1,
            is_admin=is_admin
        )

        return JsonResponse({
            "username": user.username,
            "is_admin": user.is_admin,  # Kirim status is_admin ke Flutter
            "status": True,
            "message": "User created successfully!"
        }, status=200)
    
    else:
        return JsonResponse({
            "status": False,
            "message": "Invalid request method."
        }, status=400)