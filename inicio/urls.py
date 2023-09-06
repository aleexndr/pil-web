from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_personas, name='lista_personas'),
    path('search/', views.search_personas, name= 'search_personas'),
    path('check-password/', views.check_password, name='check_password'),
    path('index/', views.index, name='index'),
    path('logout/', views.logout, name='logout'),
]