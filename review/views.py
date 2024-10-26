from django.shortcuts import render
# from products.models import Katalog
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from review.models import FoodReview
from django.http import HttpResponse, HttpResponseNotFound
from django.core import serializers
from review.forms import ReviewFoodForm
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
import random

@login_required(login_url="authentication:login")
def show_main(request):
    review = FoodReview.objects.all().order_by("-id")
    context = {
        "review": review
    }
    return render(request, 'review.html', context)

@login_required(login_url="authentication:login")
def choose_food_review(request):
    # foods = Katalog.objects.all()
    form = ReviewFoodForm(request.POST or None)

    context = {
        # 'products': foods,
        'form': form
    }

    return render(request, "choose_food.html", context)

@csrf_exempt
def add_review(request):
    if request.method == "POST":
        user = request.user
        # food_review = Katalog.objects.get(pk=request.POST.get("id"))
        rating = request.POST.get("rating")
        review_message = request.POST.get("review_message")

        # new_review = FoodReview(user=user, food_review = food_review, rating = rating, review_message = review_message)
        # new_review.save()

        return HttpResponse(b"ADDED", status=201)
    return HttpResponseNotFound()
def show_json(request):
    data = FoodReview.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

# def get_food_review(request):
    # data = Katalog.objects.all()
    # return HttpResponse(serializers.serialize("json", data), content_type="application/json")


# def get_food_review_by_id(request, id):
    # data = Katalog.objects.filter(pk=id)
    # return HttpResponse(serializers.serialize("json", data), content_type="application/json")

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
