from django import forms
from .models import ArticleEntry

class ArticleEntryForm(forms.ModelForm):
    class Meta:
        model = ArticleEntry
        fields = ["judul", "gambar", "subjudul", "konten"]