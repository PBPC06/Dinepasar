from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Favorite
from search.models import Food
from django.db.models import Count
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger(__name__)

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
    favorites = Favorite.objects.filter(user=request.user)
    favorite_categories = favorites.values_list('food__kategori', flat=True).distinct()

    recommended_foods = Food.objects.filter(
        kategori__in=favorite_categories
    ).exclude(id__in=favorites.values_list('food__id', flat=True))

    # Log data yang dikirim
    print("Recommended foods:")
    for food in recommended_foods:
        print(f"ID: {food.id}, Name: {food.nama_makanan}, Harga: {food.harga}, Rating: {food.rating}")

    data = [
        {
            'id': food.id,
            'nama_makanan': food.nama_makanan,
            'gambar': food.gambar or '',  # Gambar default kosong jika null
            'kategori': food.kategori or 'Unknown',
            'harga': food.harga or 0,  # Harga default 0 jika null
            'rating': food.rating or 0.0,  # Rating default 0.0 jika null
        }
        for food in recommended_foods
    ]
    return JsonResponse(data, safe=False)

@login_required
def favorite_list_api(request):
    favorites = Favorite.objects.filter(user=request.user)

    # Gunakan ID dari Favorite, bukan Food
    data = [
        {
            'id': fav.id,  # ID dari Favorite
            'food_id': fav.food.id,  # ID dari Food (opsional, jika diperlukan)
            'nama_makanan': fav.food.nama_makanan,
            'gambar': fav.food.gambar or '',
            'kategori': fav.food.kategori or 'Unknown',
            'harga': fav.food.harga or 0,
            'rating': fav.food.rating or 0.0,
        }
        for fav in favorites
    ]
    return JsonResponse(data, safe=False)

@csrf_exempt
@login_required
def delete_favorite_api(request, favorite_id):
    logger.debug(f"Request received: User={request.user}, Favorite ID={favorite_id}")

    if request.method == 'POST':
        try:
            # Cari Favorite berdasarkan ID dan pengguna
            favorite = get_object_or_404(Favorite, id=favorite_id, user=request.user)
            logger.debug(f"Deleting favorite: {favorite}")
            favorite.delete()
            return JsonResponse({'message': 'Item removed from favorites.'}, status=200)
        except Favorite.DoesNotExist:
            logger.warning(f"Favorite ID {favorite_id} not found for user {request.user}")
            return JsonResponse({'error': 'Favorite not found or does not belong to the user.'}, status=404)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return JsonResponse({'error': f'Error deleting favorite: {str(e)}'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
