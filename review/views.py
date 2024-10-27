from django.shortcuts import render
# from products.models import Katalog
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from review.models import FoodReview
from django.http import HttpResponse
from django.core import serializers
from review.forms import ReviewFoodForm
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Q
from search.models import Food
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags

@login_required(login_url="authentication:login")
def show_main(request):
    review = FoodReview.objects.all().order_by("-id")
    context = {
        "review": review
    }
    return render(request, 'review.html', context)

@login_required(login_url='/login')
def choose_food(request):
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

    return render(request, 'choose_food.html', {'foods': foods})

@csrf_exempt
@require_POST
@login_required(login_url='/login')
def add_review(request):
    # Hapus tag HTML dari input untuk mencegah XSS
    review_message = strip_tags(request.POST.get("review_message", ""))
    rating = request.POST.get("rating")
    food_id = request.POST.get("food_id")
    user = request.user

    # Validasi input
    if not review_message or not rating or not food_id:
        return JsonResponse({"status": "error", "message": "All fields are required."}, status=400)

    # Pastikan rating adalah angka
    try:
        rating = float(rating)  # Atau int(rating) sesuai kebutuhan
        if rating < 0 or rating > 5:
            return JsonResponse({"status": "error", "message": "Rating must be between 0 and 5."}, status=400)
    except ValueError:
        return JsonResponse({"status": "error", "message": "Invalid rating."}, status=400)

    # Pastikan `FoodReview` dan `Food` memiliki relasi yang sesuai
    try:
        # Mengambil objek food dari ID
        food = Food.objects.get(pk=food_id)
        
        # Buat review baru
        new_review = FoodReview(
            food_review=food,
            user=user,
            rating=rating,
            review_message=review_message,
        )
        new_review.save()

        return JsonResponse({"status": "success", "message": "Review added successfully."}, status=201)
    except Food.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Food not found."}, status=404)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)

def show_json(request):
    data = FoodReview.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def get_latest_reviews(request):
    latest_reviews = FoodReview.objects.all().order_by('-id')[:3]
    data = []
    for p in latest_reviews:
        each_data = {
            "image" : p.food_review.Image,
            "fullname" : p.user.userprofile.full_name,
            "FoodName" : p.food_review.FoodName,
            "FoodRestaurant" : p.food_review.FoodRestaurant,
            "reviewMessage" : p.review_message,
            "rating" : p.rating
        }
        data.append(each_data)

    return HttpResponse(json.dumps(data), content_type="application/json")
