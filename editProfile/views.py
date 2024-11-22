# editProfile/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserProfileForm
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from search.models import Food

@login_required
def edit_profile(request):
    try:
        # Cek apakah pengguna sudah memiliki data profil tambahan
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Jika tidak ada profil, buatkan profil baru
        profile = UserProfile.objects.create(user=request.user)

    # Cek apakah semua field terisi
    all_fields_filled = bool(profile.email and profile.phone and profile.about_me)

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('main:show_main')  # Redirect ke halaman utama atau lainnya
    else:
        form = UserProfileForm(instance=profile)

    # Tampilkan form dengan data kosong (jika baru pertama kali)
    context = {
        'profile': profile,
        'all_fields_filled': all_fields_filled,  # Kirim status ke template
    }
    return render(request, 'edit_profile.html', context)


@login_required
@csrf_exempt
def edit_profile_ajax(request):
    if request.method == "POST":
        email = request.POST.get("email", "")
        phone = request.POST.get("phone", "")
        about_me = request.POST.get("about_me", "")
        
        # Update user profile
        profile = request.user.profile
        profile.email = email
        profile.phone = phone
        profile.about_me = about_me
        profile.save()

        # Return updated data as JSON
        return JsonResponse({
            "email": profile.email,
            "phone": profile.phone,
            "about_me": profile.about_me,
        })

    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
@csrf_exempt
def remove_food_from_history(request, food_id):
    try:
        # Ambil makanan berdasarkan food_id
        food = Food.objects.get(id=food_id)
        profile = request.user.profile
        
        # Hapus makanan dari history
        profile.tried_foods.remove(food)
        profile.save()

        return JsonResponse({'success': True, 'message': 'Food removed from your history.'})
    
    except Food.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Food not found.'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
