from django.db.models import Avg
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseForbidden, JsonResponse
from django.views.decorators.http import require_POST
from review.models import FoodReview
from search.models import Food
from django.contrib import messages

@login_required(login_url='/login')
def show_main(request):
    user_reviews = FoodReview.objects.filter(user=request.user)
    all_reviews = FoodReview.objects.all().select_related('user', 'food')

    context = {
        'reviews': user_reviews,
        'all_reviews': all_reviews,
    }
    return render(request, 'review.html', context)

@csrf_exempt
@require_POST
@login_required(login_url='/login')
def add_review(request):
    if request.method == "POST":
        food_id = request.POST.get("food_id")
        rating = request.POST.get("rating")
        review_message = request.POST.get("review_message")

        if not food_id or not rating or not review_message:
            return JsonResponse({"status": "error", "message": "Invalid input"}, status=400)

        food = Food.objects.get(pk=food_id)

        # Cek apakah user sudah memberikan review
        if FoodReview.objects.filter(user=request.user, food=food).exists():
            JsonResponse({"status": "error", "message": "You have already reviewed this food."}, status=400)
            return redirect('review:forum')  # Halaman tujuan jika review sudah ada

        # Simpan review
        FoodReview.objects.create(
            user=request.user,
            food=food,
            rating=rating,
            review_message=review_message,
        )
        return redirect('review:forum')
            
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)

@login_required(login_url='/login')
@csrf_exempt
def edit_review(request, review_id):
    if request.method == "POST":
        review = get_object_or_404(FoodReview, id=review_id)

        # Pastikan hanya pemilik atau admin yang dapat mengedit
        if review.user != request.user and not request.user.is_admin:
            return HttpResponseForbidden("You do not have permission to edit this review.")

        # Ambil rating baru dan pesan review baru
        new_rating = request.POST.get("rating")
        new_message = request.POST.get("review_message")
        
        if new_rating is None or new_message is None:
            return JsonResponse({"status": "error", "message": "Rating and message are required."})

        # Update review dengan rating baru dan pesan baru
        review.rating = float(new_rating)
        review.review_message = new_message
        review.save()

        return JsonResponse({
            "status": "success",
            "review": {
                "id": review.id,
                "rating": review.rating,
                "review_message": review.review_message,
                "created_at": review.created_at.strftime("%d %b %Y"),
            }
        })
    return JsonResponse({"status": "error", "message": "Invalid request method."})

@login_required
def delete_review(request, review_id):
    if request.method == "POST":
        review = get_object_or_404(FoodReview, id=review_id)

        # Pastikan hanya pemilik atau admin yang dapat menghapuss
        if review.user != request.user and not request.user.is_admin:
            return HttpResponseForbidden("You do not have permission to edit this review.")

        review.delete()
        return redirect('review:forum')
    return JsonResponse({'error': 'Invalid request'}, status=400)