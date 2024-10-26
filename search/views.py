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


# Create your views here.
from search.models import Food
def get_foods(request):
    data = Food.objects.all()
    return HttpResponse(serializers.serialize("json", data),
    content_type="application/json")

@csrf_exempt
def food_search(request):
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


    # Masukkan hasil ke dalam context
    context = {
        'foods': foods,
    }
    return render(request, 'food_search.html', context)

@csrf_exempt
def owner_dashboard(request):
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

    context = {
        'foods': foods,
        'is_owner': True  # Menandakan bahwa ini adalah halaman owner
    }

    # foods = FoodForm.object.all()
    return render(request, 'owner_dashboard.html', context)



# @csrf_exempt
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

@csrf_exempt
def delete_food(request, food_id):
    food = get_object_or_404(Food, id=food_id)
    food.delete()
    return redirect('search:owner_dashboard')


def search_redirect(request):
    if request.user.is_authenticated:
        # Periksa peran pengguna menggunakan field 'role'
        if request.user.is_admin:  # Cek jika pengguna adalah owner
            return redirect('search:owner_dashboard')  # Ganti dengan nama URL untuk owner_dashboard
        else:
            return redirect('search:food_search')  # Ganti dengan nama URL untuk food_search