from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Favorite
from search.models import Food
from django.db.models import Count

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

    # Get categories of favorite foods for recommendation
    favorite_categories = favorites.values('food__kategori').annotate(count=Count('food__kategori'))

    # Fetch recommended foods from favorite categories, excluding those already in favorites
    recommended_foods = Food.objects.filter(
        kategori__in=[cat['food__kategori'] for cat in favorite_categories]
    ).exclude(id__in=[fav.food.id for fav in favorites])

    return render(request, 'favorite/favorite_list.html', {
        'favorites': favorites,
        'recommended_foods': recommended_foods
    })

def delete_favorite(request, favorite_id):
    if request.method == 'POST':
        favorite = get_object_or_404(Favorite, id=favorite_id)
        favorite.delete()
        return redirect('favorite:favorite_list') 