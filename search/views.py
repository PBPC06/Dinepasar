from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import strip_tags
from django.db.models import Q
from django.views.decorators.http import require_POST
from .models import Food
from .forms import FoodForm


def get_foods(request):
    data = Food.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


def food_search(request):
    keyword = request.GET.get('keyword', '')
    kategori = request.GET.get('kategori', '')
    harga = request.GET.get('harga', '')

    foods = Food.objects.all()

    if keyword:
        foods = foods.filter(Q(nama_makanan__icontains=keyword) | Q(restoran__icontains=keyword))
    if kategori:
        foods = foods.filter(kategori__iexact=kategori)
    if harga == 'low':
        foods = foods.filter(harga__lt=50000)
    elif harga == 'medium':
        foods = foods.filter(harga__gte=50000, harga__lte=100000)
    elif harga == 'high':
        foods = foods.filter(harga__gt=100000)

    for food in foods:
        food.full_stars = int(food.rating)
        food.empty_stars = 5 - food.full_stars

    return render(request, 'food_search.html', {'foods': foods})


def owner_required(user):
    return user.is_admin  # Adjust to match your user model


@login_required(login_url='/login')
@user_passes_test(owner_required)
def owner_dashboard(request, is_review_page=False):
    keyword = request.GET.get('keyword', '')
    kategori = request.GET.get('kategori', '')
    harga = request.GET.get('harga', '')

    query_filter = Q()
    if keyword:
        query_filter &= Q(nama_makanan__icontains=keyword) | Q(restoran__icontains=keyword)
    if kategori:
        query_filter &= Q(kategori__iexact=kategori)
    if harga == 'low':
        query_filter &= Q(harga__lt=50000)
    elif harga == 'medium':
        query_filter &= Q(harga__gte=50000, harga__lte=100000)
    elif harga == 'high':
        query_filter &= Q(harga__gt=100000)

    foods = Food.objects.filter(query_filter)

    return render(request, 'owner_dashboard.html', {'foods': foods, 'is_owner': True}, {'is_review_page': is_review_page})


@login_required(login_url='/login')
@user_passes_test(owner_required)
@csrf_exempt
@require_POST
def add_food(request):
    nama_makanan = strip_tags(request.POST.get("nama_makanan"))
    restoran = strip_tags(request.POST.get("restoran"))
    kategori = strip_tags(request.POST.get("kategori"))
    gambar = strip_tags(request.POST.get("gambar"))
    deskripsi = strip_tags(request.POST.get("deskripsi"))
    harga = request.POST.get("harga")
    rating = request.POST.get("rating")

    errors = {}
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
        errors['rating'] = "Rating tidak boleh kosong."

    if errors:
        return JsonResponse({'errors': errors}, status=400)

    Food.objects.create(
        nama_makanan=nama_makanan,
        restoran=restoran,
        kategori=kategori,
        gambar=gambar,
        deskripsi=deskripsi,
        harga=harga,
        rating=rating
    )

    return JsonResponse({'success': True})


@login_required(login_url='/login')
@user_passes_test(owner_required)
def edit_food(request, food_id):
    food = get_object_or_404(Food, pk=food_id)

    if request.method == "POST":
        form = FoodForm(request.POST, instance=food)
        if form.is_valid():
            form.save()
            return redirect('search:owner_dashboard')
    else:
        form = FoodForm(instance=food)

    return render(request, "edit_foods.html", {'form': form})


@login_required(login_url='/login')
@user_passes_test(owner_required)
def delete_food(request, food_id):
    food = get_object_or_404(Food, id=food_id)
    food.delete()
    return redirect('search:owner_dashboard')


def search_redirect(request):
    if request.user.is_authenticated:
        if request.user.is_admin:
            return redirect('search:owner_dashboard')
        else:
            return redirect('search:food_search')
    return redirect('login')
