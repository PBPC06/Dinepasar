from django.urls import path
from densiklopedia.views import show_profil, show_sejarah, show_wisata, show_budaya, show_artikel, add_artikel, show_xml, show_json, show_xml_by_id, show_json_by_id, view_artikel, delete_artikel, edit_artikel, create_article_flutter, edit_article_flutter, delete_article_flutter

app_name = 'densiklopedia'

urlpatterns = [
    path('', show_profil, name='profil'),
    path('sejarah/', show_sejarah, name='sejarah'),
    path('wisata/', show_wisata, name='wisata'),
    path('budaya/', show_budaya, name='budaya'),
    path('artikel/', show_artikel, name='artikel'),
    path('add-artikel/', add_artikel, name='add_artikel'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
    path('view/<uuid:id>/', view_artikel, name='view_artikel'),
    path('delete/<uuid:id>/', delete_artikel, name='delete_artikel'),
    path('edit/<uuid:id>/', edit_artikel, name='edit_artikel'),
    path('create-flutter/', create_article_flutter, name='create_article_flutter'),
    path('edit-flutter/<uuid:id>/', edit_article_flutter, name='edit_article_flutter'),
    path('delete-flutter/<uuid:id>/', delete_article_flutter, name='delete_article_flutter'),
]