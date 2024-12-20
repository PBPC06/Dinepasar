from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Favorite
from search.models import Food
from django.db.models import Count
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@login_required
def add_to_favorite(request):
    if request.method == "POST":
        food_id = request.POST.get('food_id')  # Get food_id from the request
        if not food_id:
            return JsonResponse({'error': 'Invalid food ID'}, status=400)
        
        food = get_object_or_404(Food, pk=food_id)
        
        # Check if the food is already in favorites to avoid duplicates
        favorite, created = Favorite.objects.get_or_create(user=request.user, food=food)
        if not created:
            return JsonResponse({'message': 'This item is already in your favorites.'}, status=200)
        
        return JsonResponse({'message': 'Food added to favorites!'}, status=201)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user)
    print(f"User favorites queryset: {favorites}")  # Debug log for favorites

    # Get categories of favorite foods for recommendation
    favorite_categories = favorites.values('food__kategori').annotate(count=Count('food__kategori'))

    # Fetch recommended foods from favorite categories, excluding those already in favorites
    recommended_foods = Food.objects.filter(
        kategori__in=[cat['food__kategori'] for cat in favorite_categories]
    ).exclude(id__in=[fav.food.id for fav in favorites])
    print(f"Recommended foods queryset: {recommended_foods}")  # Debug log for recommended foods

    return render(request, 'favorite/favorite_list.html', {
        'favorites': favorites,
        'recommended_foods': recommended_foods
    })

def delete_favorite(request, favorite_id):
    if request.method == 'POST':
        favorite = get_object_or_404(Favorite, id=favorite_id)
        favorite.delete()
        return redirect('favorite:favorite_list') 
    
def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})

@login_required
def get_recommended(request):
    # Ambil semua kategori dari makanan favorit user
    favorites = Favorite.objects.filter(user=request.user)
    print(f"User favorites queryset: {favorites}")  # Debug log for favorites in recommendations
    favorite_categories = favorites.values_list('food__kategori', flat=True).distinct()

    # Ambil makanan rekomendasi berdasarkan kategori
    recommended_foods = Food.objects.filter(kategori__in=favorite_categories).exclude(
        id__in=favorites.values_list('food__id', flat=True)
    )
    print(f"Recommended foods queryset: {recommended_foods}")  # Debug log for recommended foods

    # Serialisasi makanan yang direkomendasikan
    data = [
        {
            'id': food.id,
            'nama_makanan': food.nama_makanan,
            'gambar': food.gambar,
            'kategori': food.kategori,
            'harga': food.harga,
            'rating': food.rating,
        }
        for food in recommended_foods
    ]
    return JsonResponse(data, safe=False)

@login_required
def favorite_list_api(request):
    print(f"Logged-in user: {request.user}")  # Debug user
    favorites = Favorite.objects.filter(user=request.user)
    print(f"Favorites for {request.user}: {favorites}")  # Debug data

    data = [
        {
            'id': fav.food.id,
            'nama_makanan': fav.food.nama_makanan,
            'gambar': fav.food.gambar,
            'kategori': fav.food.kategori,
            'harga': fav.food.harga,
            'rating': fav.food.rating,
        }
        for fav in favorites
    ]
    return JsonResponse(data, safe=False)
