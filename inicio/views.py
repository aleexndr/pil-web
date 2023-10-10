
from .models import Datos
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File
from office365.runtime.client_request_exception import RequestException

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


def iniciar_sesion (request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Consulta SQL para obtener el usuario
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM datos WHERE usuario = %s AND contrasena = %s", [username, password])
            user = cursor.fetchone()
        
        if user:
            request.session['user_id'] = user[0]  # Suponiendo que el ID de usuario está en la primera columna de la tabla
            return redirect('inicio/')

        error_message = "Credenciales incorrectas. Por favor, intenta nuevamente."
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
        del request.session['user_id']  # Elimina el usuario de la sesión
        response = redirect('iniciar_sesion')
        response.delete_cookie('sessionid')  # Elimina la cookie de sesión del lado del cliente
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







def subir_archivo(request):
    
    site_url = 'https://pilperusac.sharepoint.com/sites/intranetpil-Intranet'
    username = 'alejandro.condori@pil.com.pe'
    password = 'Core5050$'
    folder_url = "/sites/intranetpil-Intranet/Documentos compartidos/Intranet/"
    
    if request.method == 'POST' and request.FILES['archivo']:
        file = request.FILES['archivo']

        try:
            ctx = ClientContext(site_url).with_user_credentials(username=username, password=password)

            try:     
                target_folder = ctx.web.get_folder_by_server_relative_url(folder_url)
                
            except RequestException as rex:
                print(f"Error al obtener la carpeta de destino: {rex}")
                return redirect('inicio')
            
            print(f'target_folder: {target_folder}')
            print(f'serverRelative: {target_folder.serverRelativeUrl}')
            
            
            with file as file_content:
                file_bytes = file_content.read()
                if target_folder is not None and target_folder.serverRelativeUrl is not None:
                    File.save_binary(ctx, file.name, file_bytes, target_folder.serverRelativeUrl + '/' + file.name)
                    ctx.execute_query()
                else:
                    print('La carpeta de destino no es válida')


            return redirect('inicio')
        
        except Exception as e:

            print(f"Error uploading file: {e}")

    return render(request, 'index.html')


