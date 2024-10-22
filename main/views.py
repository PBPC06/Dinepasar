from django.shortcuts import render, redirect 
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from main.forms import FoodEntryForm
from main.models import FoodEntry

def show_main(request):
    food_entries = FoodEntry.objects.all()
    context = {
        'test': 'test',
        'food_entries': food_entries
    }
    return render(request, "main.html", context)

def create_food_entry(request):
    form = FoodEntryForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_food_entry.html", context)
