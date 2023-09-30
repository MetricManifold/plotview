
from django.urls import path
from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path('directories/', views.directory_list, name='directory_list'),
    path('folders/<int:directory_id>/', views.folder_list, name='folder_list'),
    path('generate_picture/<int:folder_id>/', views.generate_picture_view, name='generate_picture'),
]
