from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('check-password/', views.check_password, name='check_password'),
    path('index/', views.index, name='index'),
    path('logout/', views.logout, name='logout'),
    path('upload/',views.upload_file, name='upload_file')
]