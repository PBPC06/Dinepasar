# editProfile/views.py
from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from .models import UserProfile
from .forms import UserProfileForm
from django.views.decorators.csrf import csrf_exempt # type: ignore
from django.views.decorators.http import require_POST # type: ignore
from django.utils.decorators import method_decorator # type: ignore
from django.http import JsonResponse # type: ignore
from search.models import Food
from django.shortcuts import get_object_or_404 # type: ignore
import json
from .models import CustomUser

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

# def show_json_all(request):
#     if request.user.is_authenticated:
#         data = UserProfile.objects.filter(user=request.user)
#         print(f"Authenticated user: {request.user.username}")
#         status = True  
#     else:
#         data = UserProfile.objects.all()
#         status = True 

#     user_profile = []
#     for users in data:
#         print(f"Found user profile: {users.user.username}")
#         user_data = {
#             "user_id": users.user.id,
#             "username": users.user.username,
#             "email": users.email,  
#             "phone": users.phone, 
#             "about_me": users.about_me, 
#             "tried_foods": list(users.tried_foods.values('id', 'nama_makanan'))
#         }
#         user_profile.append(user_data)

#     return JsonResponse({"status": status, "user_profile": user_profile}, safe=False)

def show_json_all(request):
    try:
        if request.user.is_authenticated:
            # Get or create profile for authenticated user
            profile, created = UserProfile.objects.get_or_create(
                user=request.user,
                defaults={
                    'email': "",
                    'phone': "",
                    'about_me': ""
                }
            )
            data = [profile]
        else:
            data = UserProfile.objects.all()

        user_profile = []
        for users in data:
            user_data = {
                "user_id": users.user.id,
                "username": users.user.username,
                "email": users.email or "",  # Convert None to empty string
                "phone": users.phone or "",
                "about_me": users.about_me or "",
                "tried_foods": list(users.tried_foods.values('id', 'nama_makanan'))
            }
            user_profile.append(user_data)

        return JsonResponse({
            "status": True,
            "user_profile": user_profile
        }, safe=False)

    except Exception as e:
        return JsonResponse({
            "status": False,
            "message": f"Error fetching profile: {str(e)}",
            "user_profile": []
        }, status=500)
    
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

@csrf_exempt
def edit_profile_flutter(request, id):
    if request.method == 'POST':

        try:
            data = json.loads(request.body)
            profile, created = UserProfile.objects.get_or_create(user=request.user)
            new_email = data.get('email', profile.email) or ""
            new_phone = data.get('phone', profile.phone) or ""
            new_about_me = data.get('about_me', profile.about_me) or ""

            profile.email = new_email
            profile.phone = new_phone
            profile.about_me = new_about_me
            profile.save()

            user_data = {
                "user_id": profile.user.id,
                "username": profile.user.username,
                "email": profile.email,
                "phone": profile.phone,
                "about_me": profile.about_me,
                "tried_foods": list(profile.tried_foods.values('id', 'nama_makanan'))
            }

            return JsonResponse({
                "status": True,
                "user_profile": user_data
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Format JSON tidak valid'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Kesalahan server: {str(e)}'}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def get_profile(request, id):
    user = get_object_or_404(CustomUser, id=id)  
    try:
        profile = UserProfile.objects.get(user=user)
        return JsonResponse({
            'email': profile.email,
            'phone': profile.phone,
            'about_me': profile.about_me,
        })
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'Profile not found'}, status=404)

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

@csrf_exempt
def remove_food_flutter(request, id, food_id):
    try:
        if request.method != 'POST':
            return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)

        user_profile = get_object_or_404(UserProfile, user__id=id)
        food = get_object_or_404(Food, id=food_id)
        user_profile.tried_foods.remove(food)
        user_profile.save()

        return JsonResponse({'success': True, 'message': f'Food {food.nama_makanan} removed from your history.'})

    except Food.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Food not found.'}, status=404)

    except UserProfile.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User profile not found.'}, status=404)

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)