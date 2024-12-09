from django.urls import path
from . import views

app_name = 'review'

urlpatterns = [
    path('', views.show_main, name='forum'),
    path('add-review/', views.add_review, name='add_review'),
    path('edit/<int:review_id>/', views.edit_review, name='edit_review'),
    path('delete-review/<int:review_id>/', views.delete_review, name='delete_review'),
    path('xml/', views.show_xml, name='show_xml'),
    path('json/', views.show_json, name='show_json'),
    path('xml/<str:id>/', views.show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', views.show_json_by_id, name='show_json_by_id'),
    path('json/user/<str:username>/', views.show_json_by_user, name='show_json_by_user'),  # Endpoint untuk ulasan berdasarkan username

]
