from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import Food
from django.http import JsonResponse
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import strip_tags
from .forms import FoodForm
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from manageData.models import CustomUser

import json
from django.http import JsonResponse

from django.db.models import Avg
from django.db.models.functions import Coalesce
from manageData.models import CustomUser
from editProfile.models import UserProfile



# Create your views here.
from search.models import Food
def get_foods(request):
    data = Food.objects.all()
    return HttpResponse(serializers.serialize("json", data),
    content_type="application/json")

@csrf_exempt
def food_search(request):

    # Jika pengguna adalah admin, redirect ke owner_dashboard
    if request.user.is_authenticated and request.user.is_admin:
        return redirect('search:owner_dashboard')

    # Ambil parameter pencarian dan filter
    keyword = request.POST.get('keyword', '')
    kategori = request.POST.get('kategori', '')
    harga = request.POST.get('harga', '')

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

    # Tambahkan rata-rata rating untuk setiap makanan
    foods = foods.annotate(
        average_rating=Coalesce(Avg('foodreview__rating'), 0.0)
    )

    # Masukkan hasil ke dalam context
    context = {
        'foods': foods,
    }
    return render(request, 'food_search.html', context)


def owner_dashboard(request):

    if request.user.is_authenticated and not request.user.is_admin:
        return redirect('search:food_search')


    keyword = request.POST.get('keyword', '')
    kategori = request.POST.get('kategori', '')
    harga = request.POST.get('harga', '')

    # Query awal: ambil semua makanan
    foods = Food.objects.all()

    # Buat query filter
    query_filter = Q()

    # Filter berdasarkan keyword (nama makanan atau restoran)
    if keyword:
        query_filter &= (Q(nama_makanan__icontains=keyword) | Q(restoran__icontains=keyword))

    # Filter berdasarkan kategori
    if kategori:
        query_filter &= Q(kategori__iexact=kategori)

    # Filter berdasarkan harga
    if harga == 'low':
        query_filter &= Q(harga__lt=50000)
    elif harga == 'medium':
        query_filter &= Q(harga__gte=50000, harga__lte=100000)
    elif harga == 'high':
        query_filter &= Q(harga__gt=100000)

    # Terapkan semua filter pada query
    foods = foods.filter(query_filter)

    # Tambahkan rata-rata rating untuk setiap makanan
    foods = foods.annotate(
    average_rating=Coalesce(Avg('foodreview__rating'), 0.0)
    )

    context = {
        'foods': foods,
        'is_owner': True  # Menandakan bahwa ini adalah halaman owner
    }

    # foods = FoodForm.object.all()
    return render(request, 'owner_dashboard.html', context)




def add_food(request):
    if request.method == "POST":
        nama_makanan = strip_tags(request.POST.get("nama_makanan"))
        restoran = strip_tags(request.POST.get("restoran"))
        kategori = strip_tags(request.POST.get("kategori"))
        gambar = strip_tags(request.POST.get("gambar")) 
        deskripsi = strip_tags(request.POST.get("deskripsi")) 
        harga = request.POST.get("harga")
        rating = request.POST.get("rating")

        errors = {}
        # Validasi input
        if not nama_makanan:
            errors['nama_makanan'] = "Nama makanan tidak boleh kosong."
        if not restoran:
            errors['restoran'] = "Nama restoran tidak boleh kosong."
        if not kategori:
            errors['kategori'] = "Kategori tidak boleh kosong."
        if not gambar:
            errors['gambar'] = "Gambar tidak boleh kosong."
        if not deskripsi:
            errors['deskripsi'] = "Deskripsi tidak boleh kosong."
        if not harga or not harga.isdigit():
            errors['harga'] = "Harga harus diisi dan berupa angka."
        if not rating:
            errors['rating'] = "Rating tidak boleh kosong"


        if errors:
            return JsonResponse({'errors': errors}, status=400)

        new_food = Food(
            nama_makanan=nama_makanan,
            restoran=restoran,
            kategori=kategori,
            gambar=gambar,
            deskripsi=deskripsi,
            harga=harga,
            rating=rating
        )
        new_food.save()

        return JsonResponse({'success': True})

    # Jika request GET, tampilkan halaman form
    return render(request, "add_food.html")


def edit_food(request, food_id):
    food = get_object_or_404(Food, pk=food_id)
    form = FoodForm(instance=food)
    if request.method == 'POST':
        form = FoodForm(request.POST, instance=food)
        if form.is_valid():
            form.save()
            # Kembalikan pesan sukses dan URL untuk pengalihan
            return JsonResponse({'redirect_url': reverse('search:owner_dashboard')})
        else:
            return JsonResponse({'errors': form.errors}, status=400)  # Kembalikan error form sebagai JSON

    return render(request, 'edit_foods.html', {'form': form, 'food': food})

def delete_food(request, food_id):
    food = get_object_or_404(Food, id=food_id)

    if request.method == 'DELETE':  # Check if the request method is DELETE
        food.delete()
        return JsonResponse({'success': True, 'message': 'Food item deleted successfully.'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request.'}, status=400)

def search_redirect(request):
    if request.user.is_authenticated:
        # print(f"User is_admin: {request.user.is_admin}")
        if request.user.is_admin:  # Cek jika pengguna adalah owner
            return redirect('search:owner_dashboard')
        if not request.user.is_admin:
            return redirect('search:food_search')

        
def fetch_foods(request):
    if request.method == "GET":
        foods = list(Food.objects.values())  # Adjust the fields as needed
        return JsonResponse(foods, safe=False)

        
def food_preview(request, pk):
    food = get_object_or_404(Food, pk=pk)
    return render(request, 'search/food_preview.html', {'food': food})

def food_detail(request, pk):
    food = get_object_or_404(Food, pk=pk)
    return render(request, 'food_detail.html', {'food': food})

@csrf_exempt
def mark_food_as_tried(request, food_id):
    # print(f"Received food_id: {food_id}")
    try:
        # Ambil objek Food berdasarkan ID
        food = Food.objects.get(id=food_id)
        profile = request.user.profile

        # Tandai makanan sebagai sudah dicoba
        profile.tried_foods.add(food)
        profile.save()

        return JsonResponse({'success': True, 'message': 'Food added to your history in profile!'})
    except Food.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Food not found'})

@csrf_exempt
def mark_food_flutter(request, id, food_id):
    print("tes")
    try:
        user_profile = get_object_or_404(UserProfile, user__id=id)
        food = get_object_or_404(Food, id=food_id)
        print(user_profile)
        print(food)
        user_profile.tried_foods.add(food)
        user_profile.save()

        return JsonResponse({'success': True, 'message': 'Food added to your history in profile!'})
    except Food.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Food not found'})


@csrf_exempt
def add_food_flutter(request):
    if request.method == 'POST':

        data = json.loads(request.body)
        new_food = Food.objects.create(
            # user=request.user,
            nama_makanan=data["nama_makanan"],
            restoran=data["restoran"],
            kategori=data["kategori"],
            gambar=data["gambar"],
            deskripsi=data["deskripsi"],
            harga=int(data["harga"]),
            rating=float(data["rating"]),
        )

        new_food.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)

@csrf_exempt
def food_search_flutter(request):
    if request.method == 'POST':
        # Get data from POST body (assuming JSON)
        data = json.loads(request.body)
        keyword = data.get('keyword', '')
        kategori = data.get('kategori', 'all')
        harga = data.get('harga', 'all')

        # Start with all food items
        foods = Food.objects.all()

        # Apply keyword filter if provided
        if keyword:
            foods = foods.filter(nama_makanan__icontains=keyword)

        # Apply category filter if not 'all'
        if kategori != 'all':
            foods = foods.filter(kategori=kategori)

        # Apply price filter if not 'all'
        if harga != 'all':
            if harga == 'di bawah Rp50.000':
                foods = foods.filter(harga__lt=50000)
            elif harga == 'Rp 50.000 - Rp 100.000':
                foods = foods.filter(harga__gte=50000, harga__lt=100000)
            elif harga == 'Di atas Rp 100.000':
                foods = foods.filter(harga__gte=100000)

        # Convert the queryset to a list of dictionaries to return as JSON
        food_data = list(foods.values())
        return JsonResponse(food_data, safe=False)

    return JsonResponse({"error": "Invalid request method"}, status=405)



@csrf_exempt
def edit_food_flutter(request, food_id):
    # print(f"Fetching data for food_id: {food_id}")  # Debugging line

    if request.method == 'GET':
        try:
            # Mengambil data makanan berdasarkan ID
            food = get_object_or_404(Food, pk=food_id)
            food_data = {
                'nama_makanan': food.nama_makanan,
                'restoran': food.restoran,
                'kategori': food.kategori,
                'gambar': food.gambar,
                'deskripsi': food.deskripsi,
                'harga': food.harga,
                'rating': food.rating,
            }
            # print(f"Food data fetched successfully: {food_data}")  # Debugging line
            return JsonResponse({'status': True, 'data': food_data}, status=200)
        except Exception as e:
            # print(f"Error fetching food data: {str(e)}")  # Debugging line
            return JsonResponse({'status': False, 'message': str(e)}, status=500)

    elif request.method == 'POST':
        try:
            # Mengambil data dari request body
            data = json.loads(request.body)
            # print(f"Decoded JSON: {data}")  # Debugging line
            food = get_object_or_404(Food, pk=food_id)

            # Update data makanan dengan data yang diterima
            food.nama_makanan = data.get('nama_makanan', food.nama_makanan)
            food.restoran = data.get('restoran', food.restoran)
            food.kategori = data.get('kategori', food.kategori)
            food.gambar = data.get('gambar', food.gambar)
            food.deskripsi = data.get('deskripsi', food.deskripsi)
            food.harga = int(data.get('harga', food.harga))
            food.rating = float(data.get('rating', food.rating))

            food.save()  # Simpan perubahan ke database

            # print("Data updated successfully!")  # Debugging line
            return JsonResponse({'status': True, 'message': 'Data berhasil diperbarui!'}, status=200)
        except json.JSONDecodeError:
            # print("Invalid JSON format received!")  # Debugging line
            return JsonResponse({'status': False, 'message': 'Invalid JSON format'}, status=400)
        except Exception as e:
            # print(f"Error updating food data: {str(e)}")  # Debugging line
            return JsonResponse({'status': False, 'message': str(e)}, status=500)

    else:
        # print("Invalid request method")  # Debugging line
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


# Fungsi delete food flutter
@csrf_exempt
def delete_food_flutter(request, food_id):
    if request.method == 'POST':
        try:
            food = get_object_or_404(Food, id=food_id)
            food.delete()
            return JsonResponse({'success': True, 'message': 'Food item deleted successfully.'})
        except ValueError:
            return JsonResponse({'success': False, 'message': 'Invalid food ID format'}, status=404)
    