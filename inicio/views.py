import hashlib
import os
from office365.sharepoint.client_context import ClientContext
from django.http import HttpResponse
from django.db import connection
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import ProgrammingError
from dotenv import load_dotenv


# Create your views here.

load_dotenv()

def usuario_autenticado(request):
    user_id = request.session.get("user_id")
    return user_id is not None


def obtener_nombre_usuario(user_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT CorreoCorporativo FROM [ATLAS].[dbo].[P01ListaTrabajadores] WHERE idTrabajador = %s", [user_id])
        row = cursor.fetchone()
        if row:
            return row[0] 
            
        else:
            return "Usuario Desconocido"


def error_autenticacion(request):
    return render(request, "autherror.html")


def iniciar_sesion (request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            with connection.cursor() as cursor:
                
                combined_string = username + password
                hashed_password = hashlib.sha256(combined_string.encode()).digest()
                
                
                cursor.execute("SELECT idTrabajador FROM [ATLAS].[06].[00Credenciales] WHERE Pass = %s ", {hashed_password})
                
                user = cursor.fetchone()
        
            if user:
                request.session['user_id'] = user[0]
                return redirect('inicio/')
            
            else:
                error_message = "Acceso denegado. El usuario o la contraseña que proporcionaste no son válidos. Por favor, verifica e intenta de nuevo."
                messages.error(request, error_message)
                
        except ProgrammingError as e:
            error_message = f"Error de base de datos: {e}"
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

        sharepoint_url = os.getenv('SHAREPOINT_URL')
        username = os.getenv('SHAREPOINT_USERNAME')
        password = os.getenv('SHAREPOINT_PASSWORD')
        sharepoint_folder = os.getenv('SHAREPOINT_FOLDER')

        ctx = ClientContext(sharepoint_url).with_user_credentials(username, password)

        try:
            target_folder = ctx.web.get_folder_by_server_relative_url(sharepoint_folder)
            target_file = target_folder.files.add(file_name, file_content)
            ctx.load(target_file)
            ctx.execute_query()
            
            success_message = "Su archivo se subio correctamente."
            messages.success(request, success_message)
            
            return redirect('inicio')
            
        except Exception as e:
            
            error_message = "El archivo seleccionado ya se ha subido."
            messages.error(request, error_message)
            
            return redirect('inicio')
    else:
        
        return HttpResponse("Archivo no encontrado.")