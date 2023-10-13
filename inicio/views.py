import hashlib
import os
from . models import Datos
from office365.sharepoint.client_context import ClientContext
from django.http import HttpResponse
from django.db import connection
from django.shortcuts import render, redirect
from django.contrib import messages


# Create your views here.

def usuario_autenticado(request):
    user_id = request.session.get("user_id")
    return user_id is not None


def obtener_nombre_usuario(user_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT usuario FROM datos WHERE id = %s", [user_id])
        row = cursor.fetchone()
        if row:
            return row[0] 
            
        else:
            return "Usuario Desconocido"


def error_autenticacion(request):
    return render(request, "autherror.html")


# def generar_salt():
#     return os.urandom(16).hex()


# def hash_con_salt(password, salt):
#     hased_password = hashlib.sha256((password + salt).encode()).hexdigest()
#     return hased_password

# def iniciar_sesion(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
        
#         # Genera un nuevo salt para cada usuario
#         salt = generar_salt()
        
#         # Hashea la contraseña ingresada con el salt
#         hashed_password = hash_con_salt(password, salt)
        
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT * FROM datos WHERE usuario = %s", [username])
#             user = cursor.fetchone()
            
#             # Verifica si el usuario existe y si la contraseña coincidida (usando el salt)
#             if user and user[2] == hash_con_salt(password, user[1]):
#                 request.session['user_id'] = user[0]
#                 return redirect('inicio/')
        
#         error_message = "Acceso denegado. El usuario o la contraseña que proporcionaste no son válidos. Por favor, verifica e intenta de nuevo."
#         messages.error(request, error_message)
    
#     return render(request, 'login.html')


def iniciar_sesion (request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM datos WHERE usuario = %s AND contrasena = %s", [username, hashed_password])
            user = cursor.fetchone()
        
        if user:
            request.session['user_id'] = user[0]
            return redirect('inicio/')

        error_message = "Acceso denegado. El usuario o la contraseña que proporcionaste no son válidos. Por favor, verifica e intenta de nuevo."
        messages.error(request, error_message)
    
    return render(request, 'login.html')


def inicio(request):
    if usuario_autenticado(request):
        user_id = request.session.get('user_id')
        user_name = obtener_nombre_usuario(user_id)
        return render(request, 'index.html', {'user_name': user_name})
    
    else:
        return redirect('error_autenticacion')


def cerrar_sesion(request):
    if usuario_autenticado(request):
        del request.session['user_id']
        response = redirect('iniciar_sesion')
        response.delete_cookie('sessionid')
        return response
    
    return redirect('iniciar_sesion')


def registro(request):
    
    return render(request, 'register.html')


def recuperar_contraseña(request):
    
    return render(request, 'resetpass.html')


def verificacion(request):
    
    return render(request, 'verifycode.html')


def cambio_contraseña(request):
    
    return render(request, 'changepass.html')


def subir_archivo_sharepoint(request):
    if request.method == 'POST' and request.FILES['archivo']:
        uploaded_file = request.FILES['archivo']
        file_name = uploaded_file.name
        file_content = uploaded_file.read()

        sharepoint_url = "https://pilperusac.sharepoint.com/sites/intranetpil-Intranet"
        username = "alejandro.condori@pil.com.pe"
        password = "Core5050$"
        sharepoint_folder = "/sites/intranetpil-Intranet/Documentos compartidos/Intranet/alejandro"

        ctx = ClientContext(sharepoint_url).with_user_credentials(username, password)

        try:
            target_folder = ctx.web.get_folder_by_server_relative_url(sharepoint_folder)
            target_file = target_folder.files.add(file_name, file_content)
            ctx.load(target_file)
            ctx.execute_query()
            
            return redirect('inicio')
            
        except Exception as e:
            return HttpResponse(f"Error uploading file: {e}")
    else:
        
        return HttpResponse("Archivo no encontrado.")