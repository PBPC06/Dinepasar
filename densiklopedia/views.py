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
            'id': article.id,
            'judul': article.judul,
            'gambar': article.gambar,
            'subjudul': article.subjudul
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

@login_required
def delete_artikel(request, id):
    article = get_object_or_404(ArticleEntry, id=id)
    if article.user != request.user and not request.user.is_superuser:
        return HttpResponseForbidden()

    article.delete()
    return redirect(reverse('densiklopedia:artikel'))

@login_required
def edit_artikel(request, id):
    article = get_object_or_404(ArticleEntry, pk=id)
    if article.user != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You do not have permission to delete this article.")

    form = ArticleEntryForm(request.POST or None, instance=article)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(reverse('densiklopedia:artikel'))

    context = {'form': form, 'article': article}
    return render(request, 'densiklopedia/edit_artikel.html', context)

@csrf_exempt
def create_article_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_article = ArticleEntry.objects.create(
            user=request.user,
            judul=data.get('judul', ''),
            subjudul=data.get('subjudul', ''),
            konten=data.get('konten', ''),
            gambar=data.get('gambar', '')
        )

        new_article.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
    
@csrf_exempt
@login_required
def edit_article_flutter(request, article_id):
    if request.method == 'GET':
        # Ambil artikel yang dimiliki oleh pengguna yang login
        article = get_object_or_404(ArticleEntry, pk=article_id, user=request.user)
        article_data = {
            'judul': article.judul,
            'subjudul': article.subjudul,
            'konten': article.konten,
            'gambar': article.gambar,
        }
        return JsonResponse(article_data, status=200)
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Ambil artikel yang dimiliki oleh pengguna yang login
            article = get_object_or_404(ArticleEntry, pk=article_id, user=request.user)
            # Update data artikel
            article.judul = data.get('judul', article.judul)
            article.subjudul = data.get('subjudul', article.subjudul)
            article.konten = data.get('konten', article.konten)
            article.gambar = data.get('gambar', article.gambar)
            article.save()
            return JsonResponse({'message': 'Artikel berhasil diperbarui!'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
    
@csrf_exempt
def delete_article_flutter(request, article_id):
    try:
        article = get_object_or_404(ArticleEntry, id=article_id)
        if request.method == 'DELETE':
            if article.user == request.user:
                article.delete()
                return JsonResponse({'success': True, 'message': 'Article deleted successfully.'})
            else:
                return JsonResponse({'success': False, 'message': 'You are not authorized to delete this article.'}, status=403)
        else:
            return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)
    except article.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Article not found.'}, status=404)