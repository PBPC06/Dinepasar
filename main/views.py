from django.shortcuts import render, redirect 
# from main.forms import FoodEntryForm
# from main.models import FoodEntry

def show_main(request):
    context = {
        'test': 'test'
    }

    return render(request, "main.html", context)
