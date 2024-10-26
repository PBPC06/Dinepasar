from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils.html import strip_tags
from django.core import serializers
# from django.contrib.auth.models import User
# from django.contrib.auth import login
from .models import ArticleEntry
from .forms import ArticleEntryForm

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
    data = ArticleEntry.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    articles = ArticleEntry.objects.filter(user=request.user)
    data = []
    for article in articles:
            data.append({
                'id': article.id,
                'judul': article.title,
                'gambar': article.image,
                'subjudul': article.subtitle
            })

    return JsonResponse(data, safe=False)

def show_xml_by_id(request, id):
    data = ArticleEntry.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    article = ArticleEntry.objects.filter(pk=id)
    if article:
        data = {
            'id': article.id,
            'judul': article.title,
            'gambar': article.image,
            'subjudul': article.subtitle
        }
        return JsonResponse(data)
    
    return JsonResponse({'error': 'Article not found'}, status=404)

@csrf_exempt
@require_POST
def add_artikel(request):
    if request.method == 'POST':
        judul = request.POST.get('judul')
        gambar = request.POST.get('gambar')
        subjudul = request.POST.get('subjudul')
        konten = request.POST.get('konten')
        # user = request.user

        artikel = ArticleEntry.objects.create(judul=judul, gambar=gambar, subjudul=subjudul, konten=konten)

        # Kembalikan artikel yang baru saja ditambahkan dalam format JSON
        return JsonResponse({
            'id': artikel.id,
            'judul': artikel.judul,
            'gambar': artikel.gambar,
            'subjudul': artikel.subjudul
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)
