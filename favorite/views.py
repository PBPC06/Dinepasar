from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import FavoriteRestaurant

# View untuk menampilkan restoran favorit
@login_required
def favorite_list(request):
    # Mengambil restoran favorit milik user yang sedang login
    favorite_restaurants = FavoriteRestaurant.objects.filter(user=request.user)
    
    # Mengirim data restoran favorit ke template favorite.html
    return render(request, 'favorite.html', {
        'favorite_restaurants': favorite_restaurants
    })

# View untuk menghapus restoran favorit
@login_required
def remove_favorite(request, restaurant_id):
    # Cari restoran favorit berdasarkan ID dan user
    restaurant = FavoriteRestaurant.objects.get(id=restaurant_id, user=request.user)
    
    # Hapus restoran tersebut
    restaurant.delete()
    
    # Redirect ke halaman favorit setelah penghapusan
    return redirect('favorite_list')
