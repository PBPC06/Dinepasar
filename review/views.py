from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.db.models import Q
from django.utils.html import strip_tags
from django.views.decorators.http import require_POST
from review.models import FoodReview
from review.forms import ReviewFoodForm
from search.models import Food
import json


@login_required(login_url="authentication:login")
def show_main(request):
    reviews = FoodReview.objects.all()  # Retrieve all reviews from the database
    return render(request, 'review.html', {'review': reviews})

@login_required(login_url='/login')
def choose_food(request):
    # Search and filter functionality
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
    if request.method == 'POST':
        food_id = request.POST.get('food_id')  # Make sure food_id is being passed
        rating = request.POST.get('food_rating')
        review_message = request.POST.get('review')

        # Create the review in your database
        # Example: FoodReview.objects.create(food_id=food_id, rating=rating, review=review_message)

        return JsonResponse({'status': 'success', 'message': 'Review added successfully'})

    # If you want to handle GET requests for any reason
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def show_json(request):
    # Return all reviews as JSON
    data = FoodReview.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


def get_latest_reviews(request):
    # Retrieve and serialize the latest reviews
    latest_reviews = FoodReview.objects.all().order_by('-id')[:3]
    data = []
    for p in latest_reviews:
        each_data = {
            "image": p.food_review.Image,
            "fullname": p.user.userprofile.full_name,
            "FoodName": p.food_review.FoodName,
            "FoodRestaurant": p.food_review.FoodRestaurant,
            "reviewMessage": p.review_message,
            "rating": p.rating
        }
        data.append(each_data)

    return HttpResponse(json.dumps(data), content_type="application/json")
