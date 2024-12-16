from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.core import serializers
from django.contrib.auth.decorators import login_required
from manageData.models import CustomUser
from .models import ArticleEntry
from .forms import ArticleEntryForm
import json

def show_profil(request):
    return render(request, 'densiklopedia/profil.html')

def show_sejarah(request):
    return render(request, 'densiklopedia/sejarah.html')

def show_wisata(request):
    return render(request, 'densiklopedia/wisata.html')

def show_budaya(request):
    return render(request, 'densiklopedia/budaya.html')

def show_artikel(request):
    articles = ArticleEntry.objects.all()
    context = {
        'artikel': articles
    }
    return render(request, 'densiklopedia/artikel.html', context)

def show_xml(request):
    data = ArticleEntry.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    articles = ArticleEntry.objects.all()
    data = [
        {
            'id': str(article.id),     
            'judul': article.judul,
            'gambar': article.gambar,
            'subjudul': article.subjudul,
            'konten': article.konten,
        }
        for article in articles
    ]
    return JsonResponse(data, safe=False)


def show_xml_by_id(request, id):
    data = ArticleEntry.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    article = ArticleEntry.objects.filter(pk=id).first()
    if article:
        data = {
            'id': article.id,
            'judul': article.judul,
            'gambar': article.gambar,
            'subjudul': article.subjudul
        }
        return JsonResponse(data)
    
    return JsonResponse({'error': 'Article not found'}, status=404)

@require_POST
@login_required
def add_artikel(request):
    form = ArticleEntryForm(request.POST)
    if form.is_valid():
        artikel = form.save(commit=False)
        artikel.user = request.user 
        artikel.save()

        return JsonResponse({
            'id': artikel.id,
            'judul': artikel.judul,
            'gambar': artikel.gambar,
            'subjudul': artikel.subjudul
        })
    return JsonResponse({'error': form.errors}, status=400)

def view_artikel(request, id):
    article = get_object_or_404(ArticleEntry, id=id)
    article.konten = article.konten.replace(' ', '&nbsp;').replace('\n', '<br>')
    return render(request, 'densiklopedia/view_artikel.html', {'article': article})

def delete_artikel(request, id):
    article = get_object_or_404(ArticleEntry, id=id)
    if article.user != request.user and not request.user.is_admin:
        return HttpResponseForbidden("You do not have permission to delte this article.")

    article.delete()
    return redirect(reverse('densiklopedia:artikel'))

def edit_artikel(request, id):
    article = get_object_or_404(ArticleEntry, pk=id)
    if article.user != request.user and not request.user.is_admin:
        return HttpResponseForbidden("You do not have permission to edit this article.")

    form = ArticleEntryForm(request.POST or None, instance=article)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(reverse('densiklopedia:artikel'))

    context = {'form': form, 'article': article}
    return render(request, 'densiklopedia/edit_artikel.html', context)

@csrf_exempt
@login_required
def create_article_flutter(request):
    if request.method == 'POST':
        # Mengakses data dari request.POST
        data = request.POST
        # Pastikan pengguna terautentikasi
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'User not authenticated'}, status=401)

        # Buat entri artikel baru
        new_article = ArticleEntry.objects.create(
            user=request.user,
            judul=data.get('judul', ''),
            subjudul=data.get('subjudul', ''),
            konten=data.get('konten', ''),
            gambar=data.get('gambar', '')
        )
        new_article.save()
        return JsonResponse({"status": "success", "id": str(new_article.id)}, status=200)
    else:
        return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)
    
@csrf_exempt
@login_required
def edit_article_flutter(request, id):
    try:
        article = get_object_or_404(ArticleEntry, id=id)

        # Periksa apakah pengguna memiliki izin untuk mengedit
        if article.user != request.user and not request.user.is_admin:
            return JsonResponse({'status': 'error', 'message': 'You do not have permission to edit this article.'}, status=403)

        if request.method == 'POST':
            data = request.POST
            article.judul = data.get('judul', article.judul)
            article.subjudul = data.get('subjudul', article.subjudul)
            article.konten = data.get('konten', article.konten)
            article.gambar = data.get('gambar', article.gambar)
            article.save()
            return JsonResponse({'message': 'Artikel berhasil diperbarui!'}, status=200)
        elif request.method == 'GET':
            article_data = {
                'judul': article.judul,
                'subjudul': article.subjudul,
                'konten': article.konten,
                'gambar': article.gambar,
            }
            return JsonResponse(article_data, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@csrf_exempt
@require_POST
def delete_article_flutter(request, id):
    try:
        article = get_object_or_404(ArticleEntry, id=id)
        
        # Periksa izin pengguna
        if article.user == request.user or request.user.is_admin:
            article.delete()
            print(f"Deleted article: {article}")  # Debugging
            return JsonResponse({'success': True, 'message': 'Article deleted successfully.'})
        else:
            return JsonResponse({'success': False, 'message': 'You are not authorized to delete this article.'}, status=403)
    except ArticleEntry.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Article not found.'}, status=404)
    except Exception as e:
        print(f"Error in delete_article_flutter: {e}")  # Debugging
        return JsonResponse({'success': False, 'message': str(e)}, status=400)