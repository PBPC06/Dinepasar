from django import forms
from .models import Food
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.utils.html import strip_tags


class SearchForm(forms.Form):
    keyword = forms.CharField(required=False, label='Cari makanan/resto', widget=forms.TextInput(attrs={
        'class': 'form-input',
        'placeholder': 'Cari makanan/resto...',
    }))


class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role', 'password1', 'password2')


class FoodForm(ModelForm):
    class Meta:
        model = Food
        fields = ["nama_makanan", "restoran", "kategori", "gambar", "deskripsi", "harga", "rating"]

    def clean_nama_makanan(self):
        nama_makanan = self.cleaned_data["nama_makanan"]
        return strip_tags(nama_makanan)

    def clean_restoran(self):
        restoran = self.cleaned_data["restoran"]
        return strip_tags(restoran)
    
    def clean_kategori(self):
        kategori = self.cleaned_data["kategori"]
        return strip_tags(kategori)

    def clean_gambar(self):
        gambar = self.cleaned_data["gambar"]
        return strip_tags(gambar)

    def clean_deskripsi(self):
        deskripsi = self.cleaned_data["deskripsi"]
        return strip_tags(deskripsi)
    
    def clean_harga(self):
        harga = self.cleaned_data["harga"]
        return strip_tags(harga)
    
    def clean_rating(self):
        rating = self.cleaned_data["rating"]
        return strip_tags(rating)
