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


# from django.http import JsonResponse
# from .models import FoodEntry

# def food_entries_json(request):
#     # Mengambil semua data dari model FoodEntry
#     food_entries = FoodEntry.objects.all().values('name', 'description', 'price', 'rating')
    
#     # Mengonversi queryset ke list dan mengembalikan sebagai JSON
#     return JsonResponse(list(food_entries), safe=False)



@csrf_exempt
def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Save the form without committing to the database yet
            
            # Set the is_admin field based on the form validation
            if form.cleaned_data.get('isAdmin'):
                user.is_admin = True
            else:
                user.is_admin = False
            
            user.save()  # Now save the user to the database
            
            messages.success(request, 'Your account has been successfully created!')
            return redirect('manageData:login')
    else:
        form = NewUserForm()  # Inisialisasi form saat method GET

    context = {'form': form}
    return render(request, 'register.html', context)


def login_user(request):
    # username = request.POST['username']
    # password = request.POST['password']
    # user = authenticate(username=username, password=password)
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

