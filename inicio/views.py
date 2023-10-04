from django.shortcuts import render, redirect
from .models import Datos
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File
from office365.runtime.client_request_exception import RequestException


# Create your views here.

def iniciar_sesion (request):
    
    return render (request, 'login.html')


def autenticacion(request):
    
    return redirect('iniciar_sesion')


def inicio(request):
    
    return render(request, 'index.html')


def cerrar_sesion(request):
        
    return redirect('iniciar_sesion')


def registro(request):
    
    return render(request, 'register.html')


def recuperar_contraseña(request):
    
    return render(request, 'resetpass.html')


def verificacion(request):
    
    return render(request, 'verifycode.html')







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


