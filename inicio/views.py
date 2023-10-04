from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.db import connections
from .models import Datos
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File
from office365.runtime.client_request_exception import RequestException




# Create your views here.

def inicio (request):
    return render (request, 'login.html')


# def search_personas (request):
#     search_query = request.GET.get('q')
#     keywords = search_query.split()
    
#     query = Q()
#     for keyword in keywords:
#         query &= (Q(usuario__icontains=keyword) | Q(appat__icontains=keyword) | Q(apmat__icontains=keyword) | Q(nombres__icontains=keyword))
        
#     personas = Datos.objects.filter(query).order_by('appat',  'apmat', 'nombres')
    
#     results = [f'{persona.appat} {persona.apmat} {persona.nombres}' for persona in personas]
    
#     ids = [persona.id for persona in personas]
    
#     return JsonResponse({'results': results, 'ids':ids})


# def check_password(request):
#     user_id = request.GET.get('id')
#     password = request.GET.get('password')

#     with connections['default'].cursor() as cursor:
#         cursor.execute("SELECT COUNT(*) FROM datos WHERE id = %s AND contrasena = %s", [user_id, password])
#         result = cursor.fetchone()[0]

#     if result == 1:
#         request.session['user_id'] = user_id
#         return JsonResponse({'password_match': True})
    
#     else:
#         return JsonResponse({'password_match': False,})


def check_password(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = Datos.objects.get(usuario=username, contrasena=password)
            # Usuario autenticado correctamente, realiza las operaciones necesarias, por ejemplo, establecer la sesión.
            request.session['user_id'] = user.id
            return HttpResponseRedirect('/index/')  # Redirige al usuario a la página de inicio después del inicio de sesión exitoso
        except Datos.DoesNotExist:
            # Usuario no encontrado o contraseña incorrecta
            return render(request, 'login.html', {'error_message': 'El usuario o la contraseña son incorrectos. Por favor, inténtelo de nuevo.'})

    return render(request, 'login.html')



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
        return redirect('inicio')
    
    return render(request, 'index.html', {'username': username})


def logout(request):
    
    if 'user_id' in request.session:
        del request.session['user_id']
        
    return redirect('lista_personas')




def upload_file(request):
    
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
                return redirect('index')
            
            print(f'target_folder: {target_folder}')
            print(f'serverRelative: {target_folder.serverRelativeUrl}')
            
            
            with file as file_content:
                file_bytes = file_content.read()
                if target_folder is not None and target_folder.serverRelativeUrl is not None:
                    File.save_binary(ctx, file.name, file_bytes, target_folder.serverRelativeUrl + '/' + file.name)
                    ctx.execute_query()
                else:
                    print('La carpeta de destino no es válida')


            return redirect('index')
        
        except Exception as e:

            print(f"Error uploading file: {e}")

    return render(request, 'index.html')


