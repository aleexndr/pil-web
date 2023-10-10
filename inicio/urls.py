from django.urls import path
from . import views

urlpatterns = [
    path('', views.iniciar_sesion, name='iniciar_sesion'),
    
    path('inicio/', views.inicio, name='inicio'),
    
    path('error_autenticacion/', views.error_autenticacion, name='error_autenticacion'),
    
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    
    path('registro/', views.registro, name='registro'),
    
    path('recuperar_contraseña/', views.recuperar_contraseña, name='recuperar_contraseña'),
    
    path('verificacion/', views.verificacion, name='verificacion'),
    
    path('subir_archivo/',views.subir_archivo, name='subir_archivo'),
    
    path('cambio_contraseña/', views.cambio_contraseña, name='cambio_contraseña')
]