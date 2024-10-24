from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import Food
from django.http import JsonResponse
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required


# Create your views here.
from search.models import Food
def get_foods(request):
    data = Food.objects.all()
    return HttpResponse(serializers.serialize("json", data),
    content_type="application/json")



def food_search(request):
    # Ambil parameter pencarian dan filter
    keyword = request.GET.get('keyword', '')
    kategori = request.GET.get('kategori', '')
    harga = request.GET.get('harga', '')

    # Query awal
    foods = Food.objects.all()

    # Filter berdasarkan keyword
    if keyword:
        foods = foods.filter(nama_makanan__icontains=keyword) | foods.filter(restoran__icontains=keyword)

    # Filter berdasarkan kategori
    if kategori:
        foods = foods.filter(kategori__iexact=kategori)

    # Filter berdasarkan harga
    if harga == 'low':
        foods = foods.filter(harga__lt=50000)
    elif harga == 'medium':
        foods = foods.filter(harga__gte=50000, harga__lte=100000)
    elif harga == 'high':
        foods = foods.filter(harga__gt=100000)


    # Calculate stars
    for food in foods:
        food.full_stars = int(food.rating)  # Full stars
        food.empty_stars = 5 - food.full_stars  # Empty stars



    # Masukkan hasil ke dalam context
    context = {
        'foods': foods,
    }
    return render(request, 'food_search.html', context)


@login_required
def add_food(request):
    if request.user.profile.is_admin:
        if request.method == 'POST':
            # Handle food creation
            new_food = Food(
                nama_makanan=request.POST['nama_makanan'],
                kategori=request.POST['kategori'],
                harga=request.POST['harga']
            )
            new_food.save()
            return redirect('food_search')
        return render(request, 'add_food.html')
    else:
        return redirect('food_search')

@login_required
def edit_food(request, pk):
    food = get_object_or_404(Food, pk=pk)
    if request.user.profile.is_admin:
        if request.method == 'POST':
            food.nama_makanan = request.POST['nama_makanan']
            food.harga = request.POST['harga']
            food.save()
            return redirect('food_search')
        return render(request, 'edit_food.html', {'food': food})
    return redirect('food_search')

@login_required
def delete_food(request, pk):
    food = get_object_or_404(Food, pk=pk)
    food.delete()
    return redirect('food_search')



def food_preview(request, pk):
    food = get_object_or_404(Food, pk=pk)
    return render(request, 'search/food_preview.html', {'food': food})




