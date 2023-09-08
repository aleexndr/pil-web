from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db import connections
from .models import Datos


# Create your views here.

def lista_personas (request):
    personas = Datos.objects.all()
    return render(request, 'login.html', {'personas': personas})


def search_personas (request):
    search_query = request.GET.get('q')
    keywords = search_query.split()
    
    query = Q()
    for keyword in keywords:
        query &= (Q(usuario__icontains=keyword) | Q(appat__icontains=keyword) | Q(apmat__icontains=keyword) | Q(nombres__icontains=keyword))
        
    personas = Datos.objects.filter(query).order_by('appat',  'apmat', 'nombres')
    
    results = [f'{persona.appat} {persona.apmat} {persona.nombres}' for persona in personas]
    
    ids = [persona.id for persona in personas]
    
    return JsonResponse({'results': results, 'ids':ids})


def check_password(request):
    user_id = request.GET.get('id')
    password = request.GET.get('password')

    with connections['default'].cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM datos WHERE id = %s AND contrasena = %s", [user_id, password])
        result = cursor.fetchone()[0]

    if result == 1:
        request.session['user_id'] = user_id
        return JsonResponse({'password_match': True})
    
    else:
        return JsonResponse({'password_match': False,})


def index(request):
    
    user_id = request.session.get('user_id', None)
    username = None
    
    if user_id:
        try:
            usuario = Datos.objects.get(id=user_id)
            username = usuario.nombres
        except Datos.DoesNotExist:
            pass
    else:
        return redirect('lista_personas')
    
    return render(request, 'index.html', {'username': username})


def logout(request):
    
    if 'user_id' in request.session:
        del request.session['user_id']
        
    return redirect('lista_personas')
