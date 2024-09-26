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
    
    path('cambio_contraseña/', views.cambio_contraseña, name='cambio_contraseña'),
    
    path('verificacion/', views.verificacion, name='verificacion'),
    
    path('solicitudes/', views.solicitudes, name='solicitudes'),
    
    path('vacaciones_solicitud/', views.vacaciones_solicitud, name='vacaciones_solicitud'),
    
    path('vacaciones_solicitud_editar/', views.vacaciones_solicitud_editar, name='vacaciones_solicitud_editar'),
    
    path('descanso_solicitud/', views.descanso_solicitud, name='descanso_solicitud'),

    path('descanso_solicitud_editar/', views.descanso_solicitud_editar, name='descanso_solicitud_editar'),
    
    path('licencia_solicitud/', views.licencia_solicitud, name='licencia_solicitud'),

    path('licencia_solicitud_editar/', views.licencia_solicitud_editar, name='licencia_solicitud_editar'),
    
    path('falta_solicitud/', views.falta_solicitud, name='falta_solicitud'),

    path('falta_solicitud_editar/', views.falta_solicitud_editar, name='falta_solicitud_editar'),
    
    path('eliminar_solicitud/<int:solicitud_id>/', views.eliminar_solicitud, name='eliminar_solicitud'),
    
    path('editar_solicitud/<int:solicitud_id>/', views.editar_solicitud, name='editar_solicitud'),
    
]