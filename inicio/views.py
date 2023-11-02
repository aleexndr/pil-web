import os
import ssl
import hashlib
import smtplib
import random
from django.db import connection
from django.db import ProgrammingError
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.datastructures import MultiValueDictKeyError
from office365.sharepoint.client_context import ClientContext
from dotenv import load_dotenv
from email.message import EmailMessage


# Create your views here.

load_dotenv()

def usuario_autenticado(request):
    user_id = request.session.get("user_id")
    return user_id is not None


def obtener_nombre_usuario(user_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT Paterno + ' ' + Materno + ' ' + Nombres AS NombreCompleto FROM [ATLAS].[dbo].[P01ListaTrabajadores] WHERE idTrabajador = %s", [user_id])
        row = cursor.fetchone()
        if row:
            return row[0] 
            
        else:
            return "Usuario Desconocido"


def error_autenticacion(request):
    return render(request, "autherror.html")


def iniciar_sesion (request):
    error_message = None
    
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
    
    delete = redirect('iniciar_sesion')
    delete.delete_cookie('sessionid')
    return delete


def registro(request):
    error_message = None
    
    if request.method == 'POST':
        appaterno = request.POST['appaterno'].upper()
        apmaterno = request.POST['apmaterno'].upper()
        name = request.POST['name'].upper()
        dni = request.POST['dni']
        date = request.POST['date']
        username = request.POST['username']
        password = request.POST['password']

        with connection.cursor() as cursor:
            cursor.execute("SELECT idTrabajador FROM [ATLAS].[dbo].[P01ListaTrabajadores] WHERE [Num Doc] = %s AND Paterno = %s AND Materno = %s AND Nombres = %s AND CAST(fecNacimiento AS DATE) = %s", [dni, appaterno, apmaterno, name, date])
            
            row = cursor.fetchone()

            if row:
                id_trabajador = row[0]

                cursor.execute("SELECT COUNT(idTrabajador) FROM [ATLAS].[06].[00Credenciales] WHERE idTrabajador = %s", [id_trabajador])
                
                num_rep = cursor.fetchone()[0]

                if num_rep == 0:
                    combined_string = username + password
                    hashed_password = hashlib.sha256(combined_string.encode()).digest()

                    cursor.execute("INSERT INTO [ATLAS].[06].[00Credenciales] (idTrabajador, Pass) VALUES (%s, %s)", [id_trabajador, hashed_password])

                    return render(request, 'registerconfirmation.html', {
                        'paterno': appaterno,
                        'nombre': name
                    })
                else:
                    error_message = "Usuario ya registrado."
            else:
                error_message = "No se encontró el usuario."
    
    return render(request, 'register.html', {'error_message': error_message})


def recuperar_contraseña(request):
    
    error_message = None
    
    if request.method == 'POST':
        appaterno = request.POST['appaterno'].upper()
        apmaterno = request.POST['apmaterno'].upper()
        name = request.POST['name'].upper()
        dni = request.POST['dni']
        date = request.POST['date']
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT idTrabajador FROM [ATLAS].[dbo].[P01ListaTrabajadores] WHERE [Num Doc] = %s AND Paterno = %s AND Materno = %s AND Nombres = %s AND CAST(fecNacimiento AS DATE) = %s", [dni, appaterno, apmaterno, name, date])
            
            row = cursor.fetchone()
            
            if row:
                id_trabajador = row[0]
                
                request.session['id_trabajador'] = id_trabajador
                
                cursor.execute("SELECT COUNT(idTrabajador) FROM [ATLAS].[06].[00Credenciales] WHERE idTrabajador = %s", [id_trabajador])
                
                num_rep = cursor.fetchone()
                
                real_num_rep = num_rep[0]
                
                
                if real_num_rep == 1:
                    
                    codigo_verificacion = ''.join(random.choice('0123456789') for _ in range(6))
                    idVigencia = 1
                            
                    with connection.cursor() as cursor:
                        
                        cursor.execute("UPDATE [06].[01CodVerificacion] SET idVigencia = 0 WHERE idTrabajador = %s AND idVigencia = %s",[id_trabajador, 1])
                        
                        
                        cursor.execute("INSERT INTO [06].[01CodVerificacion] (idTrabajador, idVigencia) OUTPUT INSERTED.IdReg VALUES (%s, %s)", [id_trabajador, idVigencia])
                        
                        idRegUltimo = cursor.fetchone()[0]
                        
                        final_idreg = f"{idRegUltimo}-{codigo_verificacion}"
                        
                        cursor.execute("UPDATE [06].[01CodVerificacion] SET CodVerif = %s WHERE idReg = %s", [final_idreg, idRegUltimo])
                        
                        cursor.execute("SELECT CorreoPersonal FROM [ATLAS].[dbo].[P01ListaTrabajadores] WHERE idTrabajador = %s", [id_trabajador])
                        
                        correo = cursor.fetchone()
                        
                        if correo:
                            correo_receptor = correo[0]
                            
                            email_sender = "irodnoc7@gmail.com"
                            password = os.getenv("PASSWORD")
                            email_reciver = "alejandrocondori0507@gmail.com"
                            subject = "Codigo de verificacion"
                            code = final_idreg
                            body = f"""
                                Estimado/a {name},
                                Para restablecer tu contraseña, utiliza el siguiente código de verificación:\n
                                Código de Verificación: {code}\n
                                Si no has solicitado este cambio, te recomendamos que contactes con nuestro equipo de soporte de inmediato.\n
                                Saludos,
                                El equipo de seguridad
                            """
                        
                            em = EmailMessage()
                            em["From"] = email_sender
                            em["To"] = email_reciver
                            em["Subject"] = subject
                            em.set_content(body)
                            
                            context = ssl.create_default_context()
                            
                            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context = context) as smtp:
                                smtp.login(email_sender, password)
                                smtp.sendmail(email_sender, email_reciver, em.as_string())
                                
                                return redirect ('verificacion')
                else:
                    error_message = "Este usuario no tiene una cuenta creada."
            else:
                error_message = "Usuario no encontrado"
           
    return render(request, 'resetpass.html', {'error_message': error_message})


def verificacion(request):
    error_message = None
    
    if request.method == 'POST':
        codigo_verificacion = request.POST['verifycode']
        
        with connection.cursor() as cursor:
            
            cursor.execute("SELECT COUNT(idReg) FROM [06].[01CodVerificacion] WHERE CodVerif = %s AND idVigencia = %s", [codigo_verificacion, 1])
            
            vigencia = cursor.fetchone()
            
            id_vig = vigencia[0]
            
            if id_vig == 1:
                cursor.execute("UPDATE [06].[01CodVerificacion] SET idVigencia = %s WHERE CodVerif = %s", [0, codigo_verificacion])
                
                return redirect("cambio_contraseña")
            
            else:
                error_message = "Código de verificación inválido o expirado. Inténtalo de nuevo o solicita un nuevo código."
                       
    return render(request, 'verifycode.html', {'error_message': error_message})


def cambio_contraseña(request):
    error_message = None
    
    if request.method == 'POST':
        new_pass = request.POST['newpass']
        conf_new_pass = request.POST['confirmnewpass']
        
        id_trabajador = request.session.get('id_trabajador')
        
        if new_pass == conf_new_pass:
            
            
            
            with connection.cursor() as cursor:
                
                cursor.execute('SELECT "Num Doc" FROM [ATLAS].[dbo].[P01ListaTrabajadores] WHERE idTrabajador = %s', [id_trabajador])
                
                dni = cursor.fetchone()
                
                if dni:
                    num_dni = dni[0]
                    
                    pass_to_hash = num_dni + conf_new_pass
                    
                    new_hash_pass = hashlib.sha256(pass_to_hash.encode()).digest()
            
                    cursor.execute("UPDATE [ATLAS].[06].[00Credenciales] SET Pass = %s WHERE idTrabajador = %s", [new_hash_pass, id_trabajador])
                    
                    return render(request, "verifyconfirmation.html")
                
                else:
                    error_message = "No se encontró el número de documento del usuario."
        
        else:
            error_message = "Las contraseñas no coinciden. Inténtalo de nuevo."
                
    return render(request, 'changepass.html', {'error_message': error_message})


def subir_archivo_sharepoint(request):
        
    if request.method == 'POST':
        try:
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
                
        except MultiValueDictKeyError:
            info_message = "Por favor, seleccione un archivo antes de intentar subirlo."
            messages.info(request, info_message)
            return redirect('inicio')
        
    else:
        return redirect('inicio')
    
    
def solicitudes(request):
    return render(request, 'inicio/solicitudes.html')