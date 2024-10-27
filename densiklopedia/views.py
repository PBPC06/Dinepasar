from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.core import serializers
from django.contrib.auth.decorators import login_required
from manageData.models import CustomUser
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
        return HttpResponseForbidden()

    form = ArticleEntryForm(request.POST or None, instance=article)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(reverse('densiklopedia:artikel'))

    context = {'form': form, 'article': article}
    return render(request, 'densiklopedia/edit_artikel.html', context)