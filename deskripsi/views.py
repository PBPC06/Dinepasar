# deskripsi/views.py

from django.shortcuts import render, get_object_or_404
from search.models import Food
from review.models import FoodReview
from django.db.models import Avg
from django.http import JsonResponse

def food_detail(request, food_id):
    food = get_object_or_404(Food, id=food_id)
    average_rating = FoodReview.objects.filter(food=food).aggregate(Avg('rating'))['rating__avg'] or 0
    reviewed_foods = FoodReview.objects.filter(user=request.user).values_list('food_id', flat=True)

    return render(request, 'deskripsi/detail.html', {'food': food, 'rating': average_rating, 'reviewed_foods': reviewed_foods})

def food_detail_api(request, food_id):
    food = get_object_or_404(Food, id=food_id)
    return JsonResponse({
        'id': food.id,
        'nama_makanan': food.nama_makanan,
        'restoran': food.restoran,
        'kategori': food.kategori,
        'gambar': food.gambar,
        'deskripsi': food.deskripsi,
        'harga': food.harga,
        'rating': food.rating,
    })