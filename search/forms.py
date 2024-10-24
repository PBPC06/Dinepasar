from django import forms
from .models import Food

class SearchForm(forms.Form):
    keyword = forms.CharField(required=False, label='Cari makanan/resto', widget=forms.TextInput(attrs={
        'class': 'form-input',
        'placeholder': 'Cari makanan/resto...',
    }))
