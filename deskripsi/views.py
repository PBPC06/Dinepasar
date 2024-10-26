# deskripsi/views.py

from django.shortcuts import render, get_object_or_404, redirect
from search.models import Food

def food_detail(request, food_id):
    food = get_object_or_404(Food, id=food_id)
    return render(request, 'deskripsi/detail.html', {'food': food})