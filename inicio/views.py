import os
import ssl
import json
import hashlib
import smtplib
import base64
import random
import datetime
from django.db import connection
from django.db import ProgrammingError, DatabaseError
from django.shortcuts import render, redirect
from django.contrib import messages
####################################
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password
from django_ratelimit.decorators import ratelimit
####################################
from django.core.files.uploadedfile import UploadedFile
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File
from dotenv import load_dotenv
from email.message import EmailMessage




# Create your views here.

load_dotenv()

# engine = create_engine('mssql+pytds://adminAtlas:C#3ntvI2ion96$$@191.98.141.245:1433/ATLAS')
# connection = engine.connect()

#MARK:USER_AUTH
def usuario_autenticado(request):   #✓
    user_id = request.session.get("user_id")
    return user_id is not None




#MARK:OBT_USER
def obtener_nombre_usuario(user_id):    #✓
    with connection.cursor() as cursor:
        cursor.execute("SELECT Paterno + ' ' + Materno + ', ' + Nombres AS NombreCompleto FROM [ATLAS].[dbo].[P01ListaTrabajadores] WHERE idTrabajador = %s", [user_id])
        row = cursor.fetchone()
        if row:
            return row[0]

        else:
            return "Usuario Desconocido"




#MARK:ERROR_AUTH
def error_autenticacion(request):   #✓
    return render(request, "autherror.html")




#MARK:INICIAR_SESION
# @ratelimit(key='ip', rate='5/120s', method=['POST', 'GET'], block=True)
def iniciar_sesion(request):
    # if getattr(request, 'limited', False):
    #     messages.error(request, "Has intentado demasiadas veces. Inténtalo de nuevo en un minuto.")
    #     return render(request, 'login.html')
    # else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            try:
                with connection.cursor() as cursor:
                    
                    combined_string = username + password
                    hashed_password = hashlib.sha256(combined_string.encode()).digest()

                    # hashed_password = make_password(password)
                    # check_password(password, hashed_password)

                    result = cursor.execute("SELECT idTrabajador FROM [ATLAS].[06].[00Credenciales] WHERE Pass = %s", [hashed_password]).fetchone()

                    if result:
                        user = result[0]
                        request.session['user_id'] = user
                        return redirect('inicio/')
                    else:
                        error_message = "Acceso denegado. El usuario o la contraseña que proporcionaste no son válidos."
                        messages.error(request, error_message)

            except ProgrammingError as e:
                error_message = f"Error de base de datos: {e}"
                messages.error(request, error_message)

        return render(request, 'login.html')




# def iniciar_sesion(request):    #✓

#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']

#         try:
#             with connection.cursor() as cursor:
                
#                 combined_string = username + password
#                 hashed_password = hashlib.sha256(combined_string.encode()).digest()

#                 # hashed_password = make_password(password)
#                 # check_password(password, hashed_password)

#                 result = cursor.execute("SELECT idTrabajador FROM [ATLAS].[06].[00Credenciales] WHERE Pass = %s", [hashed_password]).fetchone()

#                 if result:
#                     user = result[0]
#                     request.session['user_id'] = user
#                     return redirect('inicio/')
#                 else:
#                     error_message = "Acceso denegado. El usuario o la contraseña que proporcionaste no son válidos."
#                     messages.error(request, error_message)

#         except ProgrammingError as e:
#             error_message = f"Error de base de datos: {e}"
#             messages.error(request, error_message)

#     return render(request, 'login.html')



#MARK:INICIO
def inicio(request):    #✓
    if usuario_autenticado(request):
        user_id = request.session.get('user_id')
        user_name = obtener_nombre_usuario(user_id)

        try:
            with connection.cursor() as cursor:
                consulta_intermediario = cursor.execute("SELECT COUNT(idTrabajador) FROM [ATLAS].[10].[02Intermediario] WHERE idTrabajador = %s", [user_id])
                is_intermediario = consulta_intermediario.fetchone()[0]

            context_adm = {
                'user_name': user_name,
                'intermediario': is_intermediario,
                }
            
        except ProgrammingError as e:
            error_message = f"Lo sentimos hemos tenido un problema con tu usuario"
            messages.error(request, error_message)

        return render(request, 'index.html', context_adm)

    else:
        return redirect('error_autenticacion')




#MARK:CERRAR_SESION
def cerrar_sesion(request): #✓
    if usuario_autenticado(request):
        del request.session['user_id']
        response = redirect('iniciar_sesion')
        response.delete_cookie('sessionid')
        return response
    else:
        delete = redirect('iniciar_sesion')
        delete.delete_cookie('sessionid')
        return delete




#MARK:REGISTRO
def registro(request):  #✓
    error_message = None

    if request.method == 'POST':
        appaterno = request.POST['appaterno'].upper()
        apmaterno = request.POST['apmaterno'].upper()
        # name = request.POST['name'].upper()
        dni = request.POST['dni']
        date = request.POST['date']
        username = request.POST['username']
        password = request.POST['password']

        try:
            with connection.cursor() as cursor:

                result_id_trabajador = cursor.execute("SELECT idTrabajador FROM [ATLAS].[dbo].[P01ListaTrabajadores] WHERE [Num Doc] = %s AND Paterno = %s AND Materno = %s AND CAST(fecNacimiento AS DATE) = %s AND idEstado = %s", [dni, appaterno, apmaterno, date, 1]).fetchone()
                name = cursor.execute("SELECT Nombres FROM [ATLAS].[dbo].[P01ListaTrabajadores] WHERE [Num Doc] = %s AND Paterno = %s AND Materno = %s AND CAST(fecNacimiento AS DATE) = %s AND idEstado = %s", [dni, appaterno, apmaterno, date, 1]).fetchone()

                if result_id_trabajador:

                    id_trabajador = result_id_trabajador[0]

                    num_rep = cursor.execute("SELECT COUNT(idTrabajador) FROM [ATLAS].[06].[00Credenciales] WHERE idTrabajador = %s", [id_trabajador]).fetchone()[0]

                    if num_rep == 0:
                        combined_string = username + password
                        hashed_password = hashlib.sha256(combined_string.encode()).digest()

                        cursor.execute("INSERT INTO [ATLAS].[06].[00Credenciales] (idTrabajador, Pass) VALUES (%s, %s)", [id_trabajador, hashed_password])

                        return render(request, 'registerconfirmation.html', {
                            'paterno': appaterno,
                            'nombre': name
                        })
                    else:
                        error_message = "Usuario ya registrado. Intente iniciar sesion o si olvido su contraseña pruebe a cambiarla"
                        messages.error(request, error_message)
                        return redirect('registro')
                else:
                    error_message = "No se encontró el usuario. Registre los datos correctamente e intente nuevamente."
                    messages.error(request, error_message)
                    return redirect('registro')
    
        except TypeError as c:
            error_message = f"No se encontró el usuario. Registre los datos correctamente e intente nuevamente."
            messages.error(request, error_message)
            return redirect('registro')
    
    else:
        return render(request, 'register.html', {'error_message': error_message})




#MARK:RECUPERAR_PASS
def recuperar_contraseña(request):  #✓
    error_message = None

    if request.method == 'POST':
        appaterno = request.POST['appaterno'].upper()
        apmaterno = request.POST['apmaterno'].upper()
        name = request.POST['name'].upper()
        dni = request.POST['dni']
        date = request.POST['date']

        with connection.cursor() as cursor:
            row = cursor.execute("SELECT idTrabajador FROM [ATLAS].[dbo].[P01ListaTrabajadores] WHERE [Num Doc] = %s AND Paterno = %s AND Materno = %s AND Nombres = %s AND CAST(fecNacimiento AS DATE) = %s", [dni, appaterno, apmaterno, name, date]).fetchone()

            if row:
                id_trabajador = row[0]

                request.session['id_trabajador'] = id_trabajador

                real_num_rep = cursor.execute("SELECT COUNT(idTrabajador) FROM [ATLAS].[06].[00Credenciales] WHERE idTrabajador = %s", [id_trabajador]).fetchone()[0]

                if real_num_rep == 1:

                    codigo_verificacion = ''.join(random.choice('0123456789') for _ in range(6))

                    with connection.cursor() as cursor:

                        cursor.execute("UPDATE [06].[01CodVerificacion] SET idVigencia = 0 WHERE idTrabajador = %s AND idVigencia = %s",[id_trabajador, 1])

                        idRegUltimo = cursor.execute("INSERT INTO [06].[01CodVerificacion] (idTrabajador, idVigencia) OUTPUT INSERTED.IdReg VALUES (%s, %s)", [id_trabajador, 1]).fetchone()[0]
                        
                        final_idreg = f"{idRegUltimo}-{codigo_verificacion}"

                        cursor.execute("UPDATE [06].[01CodVerificacion] SET CodVerif = %s WHERE idReg = %s", [final_idreg, idRegUltimo])

                        tex_correo = cursor.execute("SELECT CorreoPersonal FROM [ATLAS].[dbo].[P01ListaTrabajadores] WHERE idTrabajador = %s", [id_trabajador]).fetchone()

                        if tex_correo:

                            correo = tex_correo[0]

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
                            error_message = "Hubo un problema con el correo registrado. Puede comunicarse con TDI para mas ayuda."
                            messages.error(request, error_message)
                            return redirect('recuperar_contraseña')
                        
                else:
                    error_message = "Este usuario aun no tiene una cuenta creada. Valide sus datos y cree una cuenta primero."
                    messages.error(request, error_message)
                    return redirect('recuperar_contraseña')
                
            else:
                error_message = "Usuario no encontrado. Intentelo nuevamente."
                messages.error(request, error_message)
                return redirect('recuperar_contraseña')
            
    else:
        return render(request, 'resetpass.html', {'error_message': error_message})




#MARK:VERIFICACION
def verificacion(request):  #✓
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
                messages.error(request, error_message)
                return redirect('verificacion')
        
    return render(request, 'verifycode.html', {'error_message': error_message})




#MARK:CAMBIAR_PASS
def cambio_contraseña(request):     #✓
    error_message = None

    if request.method == 'POST':
        new_pass = request.POST['newpass']
        conf_new_pass = request.POST['confirmnewpass']
        id_trabajador = request.session.get('id_trabajador')

        if new_pass == conf_new_pass:

            with connection.cursor() as cursor:

                dni = cursor.execute('SELECT "Num Doc" FROM [ATLAS].[dbo].[P01ListaTrabajadores] WHERE idTrabajador = %s', [id_trabajador]).fetchone()

                if dni:
                    num_dni = dni[0]
                    pass_to_hash = num_dni + conf_new_pass
                    new_hash_pass = hashlib.sha256(pass_to_hash.encode()).digest()

                    cursor.execute("UPDATE [ATLAS].[06].[00Credenciales] SET Pass = %s WHERE idTrabajador = %s", [new_hash_pass, id_trabajador])

                    return render(request, "verifyconfirmation.html")

                else:
                    error_message = "No se encontró el número de documento del usuario. Puede comunicarse con TDI para mas ayuda."
                    messages.error(request, error_message)
                    return redirect('cambio_contraseña')
        else:
            error_message = "Las contraseñas no coincidieron. Inténtelo nuevamente."
            messages.error(request, error_message)
            return redirect('cambio_contraseña')
        
    return render(request, 'changepass.html', {'error_message': error_message})




#MARK:SOLICITUDES
def solicitudes(request):    #✓

    if usuario_autenticado(request):
        user_id = request.session.get('user_id')
        user_name = obtener_nombre_usuario(user_id)
        
        try:
            with connection.cursor() as cursor:

                # Consulta para traer los nombres de los trabajadores que aparecen en (Responsable(s) de autorizacion)
                ApellidosNombres = cursor.execute("SELECT [Apellidos y Nombres] FROM [ATLAS].[dbo].[P01ListaTrabajadores] WHERE idEstado = %s", [1])
                nombres_trabajadores = [row[0] for row in ApellidosNombres.fetchall()]

                # Consulta para mostrar las solicitudes en la pantalla principal
                consulta_solicitudes = cursor.execute("SELECT idTipSolic,fecInic,fecFin, idSolic,idAprobado FROM [ATLAS].[10].[06Solicitudes] WHERE idIntermediario = %s", [user_id])
                solicitudes_usuario = consulta_solicitudes.fetchall()

                # Consulta para traer el tipo de causas del descanso
                info_causa_des = cursor.execute("SELECT idCausa, nombreCausa, idVigencia FROM [ATLAS].[10].[00CausasDescanso] WHERE idVigencia = %s", [1])
                tip_causa_des_list = info_causa_des.fetchall()

                # Consulta para saber si el usuario es administrador o no
                consulta_intermediario = cursor.execute("SELECT COUNT(idTrabajador) FROM [ATLAS].[10].[02Intermediario] WHERE idTrabajador = %s", [user_id])
                is_intermediario = consulta_intermediario.fetchone()[0]
                
                solicitudes_formateadas = []
                solicitud_usuario_ordenadas = sorted(solicitudes_usuario, key=lambda x:x[3], reverse=True)
                for solicitud in solicitud_usuario_ordenadas:
                    id_tip_solic = solicitud[0]
                    fec_inic = solicitud[1].strftime('%Y-%m-%d')
                    fec_fin = solicitud[2].strftime('%Y-%m-%d')
                    idsolic = solicitud[3]
                    idVig = solicitud[4]

                    if idVig == 0:
                        continue

                    solicitudes_formateadas.append((id_tip_solic, fec_inic, fec_fin, idsolic, user_name))
                    
                nom_causa_des_form = []
                for causa_des in tip_causa_des_list:
                    id_tip_causa_des = causa_des[0]
                    nom_causa_des = causa_des[1]
                    id_vig_des = causa_des[2]

                    if id_vig_des == 0:
                        continue

                    nom_causa_des_form.append((id_tip_causa_des, nom_causa_des))
                    
                    
                    
                datos_edt = request.session.get('contexto', {})
                id_solicitud = datos_edt.get('id_solicitud')
                tipformato = datos_edt.get('tipoformato')

                if tipformato == 1:
                    fechaedtiniciovac = datos_edt.get('feciniceditvac')
                    fechaedtfinvac = datos_edt.get('fecfineditvac')
                    nameedtaprobvac = datos_edt.get('nomaprobeditvac')
                    nameedtsolicvac = datos_edt.get('nomsoliceditvac')

                    context = {
                    'id_solicitud': id_solicitud,
                    'tipoformato': tipformato,

                    'fecinicedit': fechaedtiniciovac,
                    'fecfinedit': fechaedtfinvac,
                    'nomaprobedt': nameedtaprobvac,
                    'nomsolicedt': nameedtsolicvac,

                    'user_name': user_name,
                    'intermediario' : is_intermediario,
                    'solicitudes_usuario': solicitudes_formateadas,
                    'nombres_trabajadores': nombres_trabajadores,
                    'data_nom_causa': nom_causa_des_form
                    }

                    return render(request, 'inicio/solicitudes.html', context)
                    
                elif tipformato == 2:
                    fechaedtiniciodes = datos_edt.get('feciniceditdes')
                    fechaedtfindes = datos_edt.get('fecfineditdes')
                    causaedtdes = datos_edt.get('caudesedt')
                    caudestexedt = datos_edt.get('caudesedttex')
                    nameedtaprobdes = datos_edt.get('nomaprobeditdes')
                    nameedtsolicdes = datos_edt.get('nomsoliceditdes')
                    namearchivoexistentedes = datos_edt.get('archivos_existentesdes')

                    context = {
                    'id_solicitud': id_solicitud,
                    'tipoformato': tipformato,
                    'archivos_existentesdes': json.dumps(namearchivoexistentedes, ensure_ascii=False),
                    'fecinicedit': fechaedtiniciodes,
                    'fecfinedit': fechaedtfindes,
                    'causaedt': causaedtdes,
                    'caudesedttex': caudestexedt,
                    'nomaprobedt': nameedtaprobdes,
                    'nomsolicedt': nameedtsolicdes,
                    'user_name': user_name,
                    'intermediario' : is_intermediario,
                    'solicitudes_usuario': solicitudes_formateadas,
                    'nombres_trabajadores': nombres_trabajadores,
                    'data_nom_causa': nom_causa_des_form
                    }

                    return render(request, 'inicio/solicitudes.html', context)
                
                elif tipformato == 3:
                    fechaedtiniciolic = datos_edt.get('feciniceditlic')
                    fechaedtfinlic = datos_edt.get('fecfineditlic')
                    catedtlic = datos_edt.get('catlicedt')
                    catedtlictex = datos_edt.get('catlicedttex')
                    detedtlic = datos_edt.get('detlicedt')
                    detedtlictex = datos_edt.get('detlicedttex')
                    desedtlic = datos_edt.get('deslicedt')
                    nameedtaproblic = datos_edt.get('nomaprobeditlic')
                    nameedtsoliclic = datos_edt.get('nomsoliceditlic')
                    namearchivoexistentelic = datos_edt.get('archivos_existenteslic')

                    context = {
                    'id_solicitud': id_solicitud,
                    'tipoformato': tipformato,
                    'archivos_existenteslic': json.dumps(namearchivoexistentelic, ensure_ascii=False),
                    'fecinicedit': fechaedtiniciolic,
                    'fecfinedit': fechaedtfinlic,
                    'catlicedt': catedtlic,
                    'catlicedttex': catedtlictex,
                    'detlicedt': detedtlic,
                    'detlicedttex': detedtlictex,
                    'deslicedt': desedtlic,
                    'nomaprobedt': nameedtaproblic,
                    'nomsolicedt': nameedtsoliclic,
                    
                    'user_name': user_name,
                    'intermediario' : is_intermediario,
                    'solicitudes_usuario': solicitudes_formateadas,
                    'nombres_trabajadores': nombres_trabajadores,
                    'data_nom_causa': nom_causa_des_form
                    }

                    return render(request, 'inicio/solicitudes.html', context)
                
                elif tipformato == 4:
                    fechaedtiniciofal = datos_edt.get('feciniceditfal')
                    fechaedtfinfal = datos_edt.get('fecfineditfal')
                    cauedtfal = datos_edt.get('caufaledt')
                    cauedtfattex = datos_edt.get('caufaledttex')
                    desedtfal = datos_edt.get('desfaledt')
                    nameedtaprobfal = datos_edt.get('nomaprobeditfal')
                    nameedtsolicfal = datos_edt.get('nomsoliceditfal')

                    context = {
                    'id_solicitud': id_solicitud,
                    'tipoformato': tipformato,

                    'fecinicedit': fechaedtiniciofal,
                    'fecfinedit': fechaedtfinfal,
                    'caufaledt': cauedtfal,
                    'caufaledttex': cauedtfattex,
                    'descripedt': desedtfal,
                    'nomaprobedt': nameedtaprobfal,
                    'nomsolicedt': nameedtsolicfal,
                    
                    'user_name': user_name,
                    'intermediario' : is_intermediario,
                    'solicitudes_usuario': solicitudes_formateadas,
                    'nombres_trabajadores': nombres_trabajadores,
                    'data_nom_causa': nom_causa_des_form
                    }

                    return render(request, 'inicio/solicitudes.html', context)

                else:
                    context = {
                    'id_solicitud': id_solicitud,
                    'tipoformato': tipformato,
                    'user_name': user_name,
                    'intermediario' : is_intermediario,
                    'solicitudes_usuario': solicitudes_formateadas,
                    'nombres_trabajadores': nombres_trabajadores,
                    'data_nom_causa': nom_causa_des_form
                    }

                    return render(request, 'inicio/solicitudes.html', context)

        except DatabaseError as e:
            error_message = f"Error al obtener las solicitudes"
            messages.error(request, error_message)
            return render(request, 'inicio/solicitudes.html', context)

    else:
        return redirect('error_autenticacion')




#MARK:ELIMINAR_SOL 
def eliminar_solicitud(request, solicitud_id):  #✓
    if usuario_autenticado(request):
        user_id = request.session.get('user_id')

        try:
            with connection.cursor() as cursor:

                cursor.execute("DELETE FROM [ATLAS].[10].[06Solicitudes] WHERE idSolic = %s AND idIntermediario = %s", [solicitud_id, user_id])

                success_message = f"La solicitud se elimino correctamente"
                messages.success(request, success_message)
                return redirect('solicitudes')

        except DatabaseError as e:
            error_message = f"Error al eliminar la solicitud"
            messages.error(request, error_message)

    else:
        return redirect('error_autenticacion')




#MARK:EDITAR_SOL
def editar_solicitud(request, solicitud_id):    #✓corregir error que si el aprobador o el solicitante ya no tienen relacion con la empresa que no abra el formulario de editar solo que muestre mensaje de error
    if usuario_autenticado(request):
        user_id = request.session.get('user_id')
        id_solicitud = solicitud_id

        sharepoint_url = os.getenv('SHAREPOINT_URL')
        username = os.getenv('SHAREPOINT_USERNAME')
        password = os.getenv('SHAREPOINT_PASSWORD')
        sharepoint_folder = os.getenv('SHAREPOINT_FOLDER')

        try:
            with connection.cursor() as cursor:

                tip_form = cursor.execute("SELECT idTipSolic FROM [ATLAS].[10].[06Solicitudes] WHERE idSolic = %s AND idIntermediario = %s", [solicitud_id, user_id]).fetchone()[0]

                if tip_form == 1:

                    solvacinfo = cursor.execute("SELECT fecInic, fecFin, idAprobador, idSolicitante FROM [ATLAS].[10].[06Solicitudes] WHERE idSolic = %s AND idIntermediario = %s", [solicitud_id, user_id]).fetchall()

                    for inf_solvacinfo in solvacinfo:
                        fecini_vac_edt = inf_solvacinfo[0].strftime('%Y-%m-%d')
                        fecfin_vac_edt = inf_solvacinfo[1].strftime('%Y-%m-%d')
                        apb_vac_edt = inf_solvacinfo[2]
                        solic_vac_edt = inf_solvacinfo[3]
                    
                    nomaprobvacedit = cursor.execute("SELECT ApellidosNombres FROM [ATLAS].[dbo].[P05RelacLab] WHERE idRegTrabajador = %s AND idVigencia = %s", [apb_vac_edt, 1]).fetchone()[0]
                    
                    nomsolicvacedit = cursor.execute("SELECT ApellidosNombres FROM [ATLAS].[dbo].[P05RelacLab] WHERE idRegTrabajador = %s AND idVigencia = %s", [solic_vac_edt, 1]).fetchone()[0]

                    contexto1 = {
                        'id_solicitud': id_solicitud,
                        'tipoformato': tip_form,
                        'feciniceditvac': fecini_vac_edt,
                        'fecfineditvac': fecfin_vac_edt,
                        'nomaprobeditvac': nomaprobvacedit,
                        'nomsoliceditvac': nomsolicvacedit,
                    }
                    
                    request.session['contexto'] = contexto1
                    return redirect('solicitudes')
                        


                elif tip_form == 2:

                    soldesinfo = cursor.execute("SELECT fecInic, fecFin, idCausa, idAprobador, idSolicitante FROM [ATLAS].[10].[06Solicitudes] WHERE idSolic = %s AND idIntermediario = %s", [solicitud_id, user_id]).fetchall()

                    for inf_soldesinfo in soldesinfo:
                        fecini_des_edt = inf_soldesinfo[0].strftime('%Y-%m-%d')
                        fecfin_des_edt = inf_soldesinfo[1].strftime('%Y-%m-%d')
                        cau_des_edt = inf_soldesinfo[2]
                        if cau_des_edt == 1:
                            cau_des_edt_tex = "ENFERMEDAD"
                        elif cau_des_edt == 2:
                            cau_des_edt_tex = "ACCIDENTE"
                        elif cau_des_edt == 3:
                            cau_des_edt_tex = "OTROS"
                        else:
                            cau_des_edt_tex = "COVID-19"
                        apb_des_edt = inf_soldesinfo[3]
                        solic_des_edt = inf_soldesinfo[4]

                    nomaprobdesedit = cursor.execute("SELECT ApellidosNombres FROM [ATLAS].[dbo].[P05RelacLab] WHERE idRegTrabajador = %s AND idVigencia = %s", [apb_des_edt, 1]).fetchone()[0]
                    nomsolicdesedit = cursor.execute("SELECT ApellidosNombres FROM [ATLAS].[dbo].[P05RelacLab] WHERE idRegTrabajador = %s AND idVigencia = %s", [solic_des_edt, 1]).fetchone()[0]
                    
                    # Obtener los archivos existentes de SharePoint
                    example_name_folder_des = f"{solicitud_id}. {nomsolicdesedit}"
                    ctx_des_edt = ClientContext(sharepoint_url).with_user_credentials(username, password)
                    folder_url = f"{sharepoint_folder}/Descansos/{example_name_folder_des}"

                    # Listar archivos del directorio de SharePoint
                    folder = ctx_des_edt.web.get_folder_by_server_relative_url(folder_url)
                    files = folder.files
                    ctx_des_edt.load(files)
                    ctx_des_edt.execute_query()

                    archivos_existentes = []
                    for file in files:
                        file_name = file.properties['Name']
                        file_url = file.serverRelativeUrl

                        archivos_existentes.append({
                            'nombre_archivo': file_name,
                            'url': file_url
                        })

                    contexto2 = {
                        'id_solicitud': id_solicitud,
                        'tipoformato': tip_form,
                        'archivos_existentesdes': archivos_existentes,
                        'feciniceditdes': fecini_des_edt,
                        'fecfineditdes': fecfin_des_edt,
                        'caudesedt': cau_des_edt,
                        'caudesedttex': cau_des_edt_tex,
                        'nomaprobeditdes': nomaprobdesedit,
                        'nomsoliceditdes': nomsolicdesedit,
                    }

                    request.session['contexto'] = contexto2
                    return redirect('solicitudes')

                

                elif tip_form == 3:

                    sollicinfo = cursor.execute("SELECT fecInic, fecFin, idCategLic, idDetalleLic, descripcion, idAprobador, idSolicitante FROM [ATLAS].[10].[06Solicitudes] WHERE idSolic = %s AND idIntermediario = %s", [solicitud_id, user_id]).fetchall()

                    for inf_sollicinfo in sollicinfo:
                        fecini_lic_edt = inf_sollicinfo[0].strftime('%Y-%m-%d')
                        fecfin_lic_edt = inf_sollicinfo[1].strftime('%Y-%m-%d')
                        cat_lic_edt = inf_sollicinfo[2]
                        if cat_lic_edt == 1:
                            cat_lic_edt_tex = "LICENCIA CON GOCE DE HABER"
                        else:
                            cat_lic_edt_tex = "LICENCIA SIN GOCE DE HABER"
                        det_lic_edt = inf_sollicinfo[3]
                        if det_lic_edt == 1:
                            det_lic_edt_tex = "LICENCIA POR MATERNIDAD"
                        elif det_lic_edt == 2:
                            det_lic_edt_tex = "LICENCIA POR PATERNIDAD"
                        elif det_lic_edt == 3:
                            det_lic_edt_tex = "FALLECIMIENTO DE FAMILIAR"
                        elif det_lic_edt == 4:
                            det_lic_edt_tex = "OTROS"
                        elif det_lic_edt == 5:
                            det_lic_edt_tex = "ESTUDIOS"
                        elif det_lic_edt == 6:
                            det_lic_edt_tex = "TRAMITES DIVERSOS"
                        elif det_lic_edt == 7:
                            det_lic_edt_tex = "MOTIVOS PERSONALES"
                        elif det_lic_edt == 8:
                            det_lic_edt_tex = "PROBLEMAS DE SALUD"
                        elif det_lic_edt == 9:
                            det_lic_edt_tex = "OTROS"
                        des_lic_edt = inf_sollicinfo[4]
                        apb_lic_edt = inf_sollicinfo[5]
                        solic_lic_edt = inf_sollicinfo[6]

                    nomaproblicedit = cursor.execute("SELECT ApellidosNombres FROM [ATLAS].[dbo].[P05RelacLab] WHERE idRegTrabajador = %s AND idVigencia = %s", [apb_lic_edt, 1]).fetchone()[0]
                    nomsoliclicedit = cursor.execute("SELECT ApellidosNombres FROM [ATLAS].[dbo].[P05RelacLab] WHERE idRegTrabajador = %s AND idVigencia = %s", [solic_lic_edt, 1]).fetchone()[0]
                    
                    # Obtener los archivos existentes de SharePoint
                    example_name_folder_lic = f"{solicitud_id}. {nomsoliclicedit}"
                    ctx_lic_edt = ClientContext(sharepoint_url).with_user_credentials(username, password)
                    folder_url = f"{sharepoint_folder}/Licencias/{example_name_folder_lic}"

                    # Listar archivos del directorio de SharePoint
                    folder_lic = ctx_lic_edt.web.get_folder_by_server_relative_url(folder_url)
                    files_lic = folder_lic.files
                    ctx_lic_edt.load(files_lic)
                    ctx_lic_edt.execute_query()

                    archivos_existenteslic = []
                    for filelic in files_lic:
                        file_name_lic = filelic.properties['Name']
                        file_url_lic = filelic.serverRelativeUrl

                        archivos_existenteslic.append({
                            'nombre_archivo': file_name_lic,
                            'url': file_url_lic
                        })

                    contexto3 = {
                        'id_solicitud': id_solicitud,
                        'tipoformato': tip_form,
                        'archivos_existenteslic': archivos_existenteslic,
                        'feciniceditlic': fecini_lic_edt,
                        'fecfineditlic': fecfin_lic_edt,
                        'catlicedt': cat_lic_edt,
                        'catlicedttex': cat_lic_edt_tex,
                        'detlicedt': det_lic_edt,
                        'detlicedttex': det_lic_edt_tex,
                        'deslicedt': des_lic_edt,
                        'nomaprobeditlic': nomaproblicedit,
                        'nomsoliceditlic': nomsoliclicedit,
                    }
                    
                    request.session['contexto'] = contexto3
                    return redirect('solicitudes')
                


                elif tip_form == 4:

                        solfalinfo = cursor.execute("SELECT fecInic, fecFin, idCausaFalt, descripcion, idAprobador, idSolicitante FROM [ATLAS].[10].[06Solicitudes] WHERE idSolic = %s AND idIntermediario = %s", [solicitud_id, user_id]).fetchall()

                        for inf_solfalinfo in solfalinfo:
                            fecini_fal_edt = inf_solfalinfo[0].strftime('%Y-%m-%d')
                            fecfin_fal_edt = inf_solfalinfo[1].strftime('%Y-%m-%d')
                            cau_fal_edt = inf_solfalinfo[2]
                            if cau_fal_edt == 1:
                                cau_fal_edt_tex = "INASISTENCIA"
                            elif cau_fal_edt == 2:
                                cau_fal_edt_tex = "JORNADA LABORAL INCOMPLETA"
                            else:
                                cau_fal_edt_tex = "OTROS"
                            des_fal_edt = inf_solfalinfo[3]
                            apb_fal_edt = inf_solfalinfo[4]
                            solic_fal_edt = inf_solfalinfo[5]

                        nomaprobfaledit = cursor.execute("SELECT ApellidosNombres FROM [ATLAS].[dbo].[P05RelacLab] WHERE idRegTrabajador = %s AND idVigencia = %s", [apb_fal_edt, 1]).fetchone()[0]
                        nomsolicfaledit = cursor.execute("SELECT ApellidosNombres FROM [ATLAS].[dbo].[P05RelacLab] WHERE idRegTrabajador = %s AND idVigencia = %s", [solic_fal_edt, 1]).fetchone()[0]
                        

                        contexto4 = {
                            'id_solicitud': id_solicitud,
                            'tipoformato': tip_form,
                            'feciniceditfal': fecini_fal_edt,
                            'fecfineditfal': fecfin_fal_edt,
                            'caufaledt': cau_fal_edt,
                            'caufaledttex': cau_fal_edt_tex,
                            'desfaledt': des_fal_edt,
                            'nomaprobeditfal': nomaprobfaledit,
                            'nomsoliceditfal': nomsolicfaledit,
                        }
                        
                        request.session['contexto'] = contexto4
                        return redirect('solicitudes')
                
                else:
                    print(tip_form)
                    error_message = "Error con el tipo de formulario"
                    messages.error(request, error_message)
                    return redirect('solicitudes')

        except (DatabaseError, TypeError) as e:
            error_message = "Error al encontrar la solicitud"
            messages.error(request, error_message)
            return redirect('solicitudes')

    else:
        return redirect('error_autenticacion')




#MARK:F.VACACIONES
def vacaciones_solicitud (request):  #✓

    if usuario_autenticado(request):

        if request.method == 'POST':
            feccreacionvac = datetime.date.today()
            idresponsablevac = request.session.get('user_id')
            fecinicvac = request.POST['fecinicvac']
            fecfinvac = request.POST['fecfinvac']
            nameaprobvac = request.POST['aprobadorvac']
            namesolicvac =  request.POST['solicitantevac']
            tiposolicvac = request.POST['tiposolicvac']

            try:
                with connection.cursor() as cursor:
                    idsolicitantevac = cursor.execute("SELECT idRegTrabajador FROM [dbo].[P05RelacLab] WHERE ApellidosNombres = %s AND idVigencia = %s", [namesolicvac, 1]).fetchone()[0]

                    rlsolicitantevac = cursor.execute("SELECT idRegRelacLab FROM [dbo].[P05RelacLab] WHERE ApellidosNombres = %s AND idVigencia = %s", [namesolicvac, 1]).fetchone()[0]

                    idaprobadorvac = cursor.execute("SELECT idRegTrabajador FROM [dbo].[P05RelacLab] WHERE ApellidosNombres = %s AND idVigencia = %s", [nameaprobvac, 1]).fetchone()[0]

                    cursor.execute("INSERT INTO [ATLAS].[10].[06Solicitudes] (idIntermediario, idSolicitante, rlSolicitante, idAprobador, idTipSolic, fecInic, fecFin, fecCreacion, idAprobado) OUTPUT INSERTED.idSolic VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",[idresponsablevac, idsolicitantevac, rlsolicitantevac, idaprobadorvac, tiposolicvac, fecinicvac, fecfinvac, feccreacionvac, 1])

                    success_message = f"Su solicitud se ha creado correctamente"
                    messages.success(request, success_message)
                    return redirect('solicitudes')

            except TypeError as a:
                error_message = f"Error al crear la solicitud"
                messages.error(request, error_message)
            except DatabaseError as e:
                error_message = f"Error al crear la solicitud"
                messages.error(request, error_message)
        else:
            error_message = f"Ha realizado un metodo de pedido inhabilitado"
            messages.error(request, error_message)
            return redirect('solicitudes')
    else:
        return redirect('error_autenticacion')
    
    

    
#MARK:F.E.VACACIONES
def vacaciones_solicitud_editar (request):  #✓

    if usuario_autenticado(request):

        if request.method == 'POST':
            feccreacionvacedt = datetime.date.today()
            idresponsablevacedt = request.session.get('user_id')
            fecinicvacedt = request.POST['fecinicvacedt']
            fecfinvacedt = request.POST['fecfinvacedt']
            nameaprobvacedt = request.POST['aprobadorvacedt']
            namesolicvacedt =  request.POST['solicitantevacedt']
            idsolicvacedt = request.POST['idsolicvacedt']

            try:
                with connection.cursor() as cursor:

                    idsolicitantevacedt = cursor.execute("SELECT idRegTrabajador FROM [dbo].[P05RelacLab] WHERE ApellidosNombres = %s AND idVigencia = %s", [namesolicvacedt, 1]).fetchone()[0]

                    rlsolicitantevacedt = cursor.execute("SELECT idRegRelacLab FROM [dbo].[P05RelacLab] WHERE ApellidosNombres = %s AND idVigencia = %s", [namesolicvacedt, 1]).fetchone()[0]

                    idaprobadorvacedt = cursor.execute("SELECT idRegTrabajador FROM [dbo].[P05RelacLab] WHERE ApellidosNombres = %s AND idVigencia = %s", [nameaprobvacedt, 1]).fetchone()[0]

                    cursor.execute("UPDATE [ATLAS].[10].[06Solicitudes] SET idIntermediario = %s, idSolicitante = %s, rlSolicitante = %s, idAprobador = %s, fecInic = %s, fecFin = %s, fecCreacion = %s WHERE idSolic = %s AND idAprobado = %s",[idresponsablevacedt, idsolicitantevacedt, rlsolicitantevacedt, idaprobadorvacedt, fecinicvacedt, fecfinvacedt, feccreacionvacedt, idsolicvacedt, 1])

                    success_message = f"Su solicitud se ha editado correctamente"
                    messages.success(request, success_message)
                    return redirect('solicitudes')

            except TypeError as a:
                error_message = f"Error al editar la solicitud"
                messages.error(request, error_message)

            except DatabaseError as e:
                error_message = f"Error al editar la solicitud"
                messages.error(request, error_message)
        else:
            error_message = f"Ha realizado un metodo de pedido inhabilitado"
            messages.error(request, error_message)
            return redirect('solicitudes')
    else:
        return redirect('error_autenticacion')




#MARK:F.DESCANSO
def descanso_solicitud(request):    #✓

    if usuario_autenticado(request):

        if request.method == 'POST':
            feccreaciondes = datetime.date.today()
            idresponsabledes = request.session.get('user_id')
            fecinicdes = request.POST['fecinicdes']
            fecfindes = request.POST['fecfindes']
            causasdes = request.POST['causasdes']
            nameaprobdes = request.POST['aprobadordes']
            namesolicdes = request.POST['solicitantedes']
            tiposolicdes = request.POST['tiposolicdes']
            solicdes = request.POST['solicitantedes']
            
            uploaded_files_des = request.FILES.getlist('archivosdes')
            sharepoint_url_des = os.getenv('SHAREPOINT_URL')
            username = os.getenv('SHAREPOINT_USERNAME')
            password = os.getenv('SHAREPOINT_PASSWORD')
            sharepoint_folder_des = os.getenv('SHAREPOINT_FOLDER')

            # Extensiones permitidas
            allowed_extensions = ['pdf', 'jpg', 'jpeg', 'png']

            try:
                with connection.cursor() as cursor:

                    idsolicitantedes = cursor.execute("SELECT idRegTrabajador FROM [dbo].[P05RelacLab] WHERE ApellidosNombres = %s AND idVigencia = %s", [namesolicdes, 1]).fetchone()[0]
                    rlsolicitantedes = cursor.execute("SELECT idRegRelacLab FROM [dbo].[P05RelacLab] WHERE ApellidosNombres = %s AND idVigencia = %s", [namesolicdes, 1]).fetchone()[0]
                    idaprobadordes = cursor.execute("SELECT idRegTrabajador FROM [dbo].[P05RelacLab] WHERE ApellidosNombres = %s AND idVigencia = %s", [nameaprobdes, 1]).fetchone()[0]
                    id_output_des = cursor.execute("INSERT INTO [ATLAS].[10].[06Solicitudes] (idIntermediario, idSolicitante, rlSolicitante, idAprobador, idTipSolic, fecInic, fecFin, fecCreacion, idCausa, idAprobado) OUTPUT INSERTED.idSolic VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",[idresponsabledes, idsolicitantedes, rlsolicitantedes, idaprobadordes, tiposolicdes, fecinicdes, fecfindes, feccreaciondes, causasdes, 1]).fetchone()[0]

                    example_name_folder = f"{id_output_des}. {solicdes}"
                    id_insert_descanso = example_name_folder

                    if id_insert_descanso:

                        try:
                            ctx_des = ClientContext(sharepoint_url_des).with_user_credentials(username, password)

                            target_folder_url_des = f"{sharepoint_folder_des}/Descansos/{id_insert_descanso}"
                            ctx_des.web.folders.add(target_folder_url_des)


                            for uploaded_file in uploaded_files_des:

                                if isinstance(uploaded_file, UploadedFile):
                                    file_name_des = uploaded_file.name
                                    file_extension = file_name_des.split('.')[-1].lower()
                                    
                                    # Validar extensión de archivo
                                    if file_extension not in allowed_extensions:
                                        error_message = f"El archivo '{file_name_des}' no tiene una extensión permitida. Solo se permiten archivos: {', '.join(allowed_extensions)}."
                                        messages.error(request, error_message)
                                        return redirect('solicitudes')
                                    
                                    else:
                                        file_content_des = uploaded_file.read()

                                    try:
                                        ctx_des.web.get_folder_by_server_relative_url(target_folder_url_des).files.add(file_name_des, file_content_des)
                                        #target_file_des = ctx_des.web.get_folder_by_server_relative_url(target_folder_url_des).files.add(file_name_des, file_content_des)
                                        # ctx_des.load(target_file_des)
                                        # ctx_des.execute_query()


                                    except Exception as e:
                                        error_message = f"Error al subir el archivo"
                                        messages.error(request, error_message)

                            try:
                                ctx_des.execute_query()  
                                success_message = f"Su solicitud se ha creado correctamente"
                                messages.success(request, success_message)
                                return redirect('solicitudes')

                            except Exception as e:
                                error_message = f"Error al subir los archivos"
                                messages.error(request, error_message)
                                return redirect('solicitudes')

                            # success_message = f"Su solicitud se ha creado correctamente"
                            # messages.success(request, success_message)
                            # return redirect('solicitudes')

                        except Exception as e:
                            error_message = "Error al subir los archivos"
                            messages.error(request, error_message)

                    else:
                        error_message = "Error al crear la carpeta de los archivos"
                        messages.error(request, error_message)
                        return redirect('solicitudes')

            except TypeError as t:
                error_message = "Error al crear la solicitud"
                messages.error(request, error_message)

            except DatabaseError as d:
                error_message = "Error al crear la solicitud"
                messages.error(request, error_message)

        else:
            error_message = "Ha realizado un metodo de pedido inhabilitado"
            messages.error(request, error_message)
            return redirect('solicitudes')

    else:
        return redirect('error_autenticacion')




#MARK:F.E.DESCANSO
def descanso_solicitud_editar(request):     #✓

    if usuario_autenticado(request):

        if request.method == 'POST':
            feccreaciondesedt = datetime.date.today()
            idresponsabledesedt = request.session.get('user_id')
            fecinicdesedt = request.POST['fecinicdesedt']
            fecfindesedt = request.POST['fecfindesedt']
            causasdesedt = request.POST['causasdesedt']
            nameaprobdesedt = request.POST['aprobadordesedt']
            namesolicdesedt = request.POST['solicitantedesedt']
            idsolicdesedt = request.POST['idsolicdesedt']

            urls_archivos_eliminar = json.loads(request.POST.get('urlsArchivosEliminar', '[]'))
            archivos_nuevos = request.FILES.getlist('archivosdesedt')
            sharepoint_url_des_edt = os.getenv('SHAREPOINT_URL')
            username_edt = os.getenv('SHAREPOINT_USERNAME')
            password_edt = os.getenv('SHAREPOINT_PASSWORD')
            sharepoint_folder_des_edt = os.getenv('SHAREPOINT_FOLDER')

            allowed_extensions_des_edt = ['pdf', 'jpg', 'jpeg', 'png']


            try:
                with connection.cursor() as cursor:

                    idsolicitantedesedt = cursor.execute("SELECT idRegTrabajador FROM [dbo].[P05RelacLab] WHERE ApellidosNombres = %s AND idVigencia = %s", [namesolicdesedt, 1]).fetchone()[0]
                    rlsolicitantedesedt = cursor.execute("SELECT idRegRelacLab FROM [dbo].[P05RelacLab] WHERE ApellidosNombres = %s AND idVigencia = %s", [namesolicdesedt, 1]).fetchone()[0]
                    idaprobadordesedt = cursor.execute("SELECT idRegTrabajador FROM [dbo].[P05RelacLab] WHERE ApellidosNombres = %s AND idVigencia = %s", [nameaprobdesedt, 1]).fetchone()[0]

                    cursor.execute("UPDATE [ATLAS].[10].[06Solicitudes] SET idIntermediario = %s, idSolicitante = %s, rlSolicitante = %s, idAprobador = %s, fecInic = %s, fecFin = %s, fecCreacion = %s, idCausa = %s WHERE idSolic = %s AND idAprobado = %s",[idresponsabledesedt, idsolicitantedesedt, rlsolicitantedesedt, idaprobadordesedt, fecinicdesedt, fecfindesedt, feccreaciondesedt, causasdesedt, idsolicdesedt, 1])

                    id_insert_descanso_edt = f"{idsolicdesedt}. {namesolicdesedt}"

                    try:
                        ctx_des_edt = ClientContext(sharepoint_url_des_edt).with_user_credentials(username_edt, password_edt)
                        target_folder_url_des_edt = f"{sharepoint_folder_des_edt}/Descansos/{id_insert_descanso_edt}"

                        for url in urls_archivos_eliminar:
                            file_to_delete = ctx_des_edt.web.get_file_by_server_relative_url(url)
                            file_to_delete.delete_object()
                        # ctx_des.execute_query()

                    except Exception as e:
                        error_message = f"Error al eliminar archivos existentes en SharePoint"
                        messages.error(request, error_message)
                        return redirect('solicitudes')


                    for archivo_nuevo_des_edt  in archivos_nuevos:

                        try:
                            file_name_des_edt = archivo_nuevo_des_edt.name
                            file_extension_des_edt = file_name_des_edt.split('.')[-1].lower()

                            if file_extension_des_edt not in allowed_extensions_des_edt:
                                error_message = f"El archivo '{file_name_des_edt}' no tiene una extensión permitida."
                                messages.error(request, error_message)
                                return redirect('solicitudes')
                                    
                            else:
                                file_content_des_edt = archivo_nuevo_des_edt.read()

                            try:
                                ctx_des_edt.web.get_folder_by_server_relative_url(target_folder_url_des_edt).files.add(file_name_des_edt, file_content_des_edt)
                                # target_file_des_edt = ctx_des.web.get_folder_by_server_relative_url(target_folder_url_des_edt).files.add(file_name_des_edt, file_content_des_edt)
                                # ctx_des.load(target_file_des_edt)
                                # ctx_des.execute_query()
                            
                            except Exception as e:
                                error_message = f"Error al subir los archivos"
                                messages.error(request, error_message)
                                return redirect('solicitudes')

                        except Exception as e:
                            error_message = f"Archivos no encontrados"
                            messages.error(request, error_message)
                            return redirect('solicitudes')
                        
                    try:
                        ctx_des_edt.execute_query()  
                        success_message = f"Su solicitud se ha creado correctamente"
                        messages.success(request, success_message)
                        return redirect('solicitudes')

                    except Exception as e:
                        error_message = f"Error al subir los archivos"
                        messages.error(request, error_message)
                        return redirect('solicitudes')

            except (TypeError, DatabaseError) as t:
                error_message = f"Error al editar la solicitud"
                messages.error(request, error_message)

        else:
            error_message = f"Ha realizado un metodo de pedido inhabilitado"
            messages.error(request, error_message)
            return redirect('solicitudes')

    else:
        return redirect('error_autenticacion')




#MARK:F.LICENCIA
def licencia_solicitud(request):    #✓

    if usuario_autenticado(request):

        if request.method == 'POST':
            FecCreacionlic = datetime.date.today()
            idResponsablelic = request.session.get('user_id')
            FecIniclic = request.POST['feciniclic']
            FecFinlic = request.POST['fecfinlic']
            TipLic = request.POST['tiplic']
            DetLic = request.POST['detlic']
            DescripLic = request.POST['deslic']
            nameaproblic = request.POST['aprobadorlic']
            TipoSoliclic = request.POST['tiposoliclic']
            namesoliclic = request.POST['solicitantelic']
            uploaded_files_lic = request.FILES.getlist('archivoslic')
            sharepoint_url_lic = os.getenv('SHAREPOINT_URL')
            username_lic = os.getenv('SHAREPOINT_USERNAME')
            password_lic = os.getenv('SHAREPOINT_PASSWORD')
            sharepoint_folder_lic = os.getenv('SHAREPOINT_FOLDER')

            allowed_extensions_lic = ['pdf', 'jpg', 'jpeg', 'png', 'docx']

            try:
                with connection.cursor() as cursor:

                    idsolicitantelic = cursor.execute("SELECT idRegTrabajador FROM [dbo].[P05RelacLab] WHERE ApellidosNombres = %s AND idVigencia = %s", [namesoliclic, 1]).fetchone()[0]

                    rlsolicitantelic = cursor.execute("SELECT idRegRelacLab FROM [dbo].[P05RelacLab] WHERE ApellidosNombres = %s AND idVigencia = %s", [namesoliclic, 1]).fetchone()[0]

                    idAprobador3 = cursor.execute("SELECT idRegTrabajador FROM [dbo].[P05RelacLab] WHERE ApellidosNombres = %s AND idVigencia = %s", [nameaproblic, 1]).fetchone()[0]

                    id_output_lic = cursor.execute("INSERT INTO [ATLAS].[10].[06Solicitudes] (idIntermediario, idSolicitante, rlSolicitante, idAprobador, idTipSolic, fecInic, fecFin, fecCreacion, idCategLic, idDetalleLic, descripcion, idAprobado) OUTPUT INSERTED.idSolic VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",[idResponsablelic, idsolicitantelic, rlsolicitantelic, idAprobador3, TipoSoliclic, FecIniclic, FecFinlic, FecCreacionlic, TipLic, DetLic, DescripLic, 1]).fetchone()[0]

                    ex_name_folder_lic = f"{id_output_lic}. {namesoliclic}"
                    id_insert_licencia = ex_name_folder_lic

                    if id_insert_licencia:

                        try:
                            ctx_lic = ClientContext(sharepoint_url_lic).with_user_credentials(username_lic, password_lic)

                            target_folder_url_lic = f"{sharepoint_folder_lic}/Licencias/{id_insert_licencia}"
                            ctx_lic.web.folders.add(target_folder_url_lic)

                            for uploaded_file_lic in uploaded_files_lic:
                                
                                if isinstance(uploaded_file_lic, UploadedFile):
                                    file_name_lic = uploaded_file_lic.name
                                    file_extension_lic = file_name_lic.split('.')[-1].lower()

                                    if file_extension_lic not in allowed_extensions_lic:
                                        error_message = f"El archivo '{file_name_lic}' no tiene una extensión permitida."
                                        messages.error(request, error_message)
                                        return redirect('solicitudes')
                                    
                                    else:
                                        file_content_lic = uploaded_file_lic.read()

                                    try:
                                        ctx_lic.web.get_folder_by_server_relative_url(target_folder_url_lic).files.add(file_name_lic, file_content_lic)
                                        # target_file_lic = ctx_lic.web.get_folder_by_server_relative_url(target_folder_url_lic).files.add(file_name_lic, file_content_lic)
                                        # ctx_lic.load(target_file_lic)
                                        # ctx_lic.execute_query()

                                    except Exception as e:
                                        error_message = "Error al subir el archivo"
                                        messages.error(request, error_message)

                                else:
                                    error_message = "Error al encontrar el archivo"
                                    messages.error(request, error_message)
                                    return redirect('solicitudes')
                            
                            try:
                                ctx_lic.execute_query()  
                                success_message = f"Su solicitud se ha creado correctamente"
                                messages.success(request, success_message)
                                return redirect('solicitudes')

                            except Exception as e:
                                error_message = f"Error al subir los archivos"
                                messages.error(request, error_message)
                                return redirect('solicitudes')

                        except Exception as e:
                            error_message = "Error al subir los archivos"
                            messages.error(request, error_message)
                    
                    else:
                        error_message = "Error al crear la carpeta de los archivos"
                        messages.error(request, error_message)
                        return redirect('solicitudes')
                    
            except (TypeError, DatabaseError):
                error_message = "Error al crear la solicitud"
                messages.error(request, error_message)

        else:
            error_message = "Ha realizado un metodo de pedido inhabilitado"
            messages.error(request, error_message)
            return redirect('solicitudes')

    else:
        return redirect('error_autenticacion')




#MARK:F.E.LICENCIA
def licencia_solicitud_editar(request):    #✓

    if usuario_autenticado(request):

        if request.method == 'POST':
            FecCreacionlicedt = datetime.date.today()
            idResponsablelicedt = request.session.get('user_id')
            FecIniclicedt = request.POST['feciniclicedt']
            FecFinlicedt = request.POST['fecfinlicedt']
            TipLicedt = request.POST['tiplicedt']
            DetLicedt = request.POST['detlicedt']
            DescripLicedt = request.POST['deslicedt']
            nameaproblicedt = request.POST['aprobadorlicedt']
            namesoliclicedt = request.POST['solicitantelicedt']
            idsoliclicedt = request.POST['idsoliclicedt']

            urls_archivos_eliminar_lic = json.loads(request.POST.get('urlsArchivosEliminarlic', '[]'))
            archivos_nuevos_lic = request.FILES.getlist('archivoslicedt')
            sharepoint_url_lic_edt = os.getenv('SHAREPOINT_URL')
            username_edt_lic = os.getenv('SHAREPOINT_USERNAME')
            password_edt_lic = os.getenv('SHAREPOINT_PASSWORD')
            sharepoint_folder_lic_edt = os.getenv('SHAREPOINT_FOLDER')

            allowed_extensions_lic_edt = ['pdf', 'jpg', 'jpeg', 'png', 'docx']

            try:
                with connection.cursor() as cursor:

                    idsolicitantelicedt = cursor.execute("SELECT idRegTrabajador FROM [dbo].[P05RelacLab] WHERE ApellidosNombres = %s AND idVigencia = %s", [namesoliclicedt, 1]).fetchone()[0]

                    rlsolicitantelicedt = cursor.execute("SELECT idRegRelacLab FROM [dbo].[P05RelacLab] WHERE ApellidosNombres = %s AND idVigencia = %s", [namesoliclicedt, 1]).fetchone()[0]

                    idAprobador3edt = cursor.execute("SELECT idRegTrabajador FROM [dbo].[P05RelacLab] WHERE ApellidosNombres = %s AND idVigencia = %s", [nameaproblicedt, 1]).fetchone()[0]
                    
                    cursor.execute("UPDATE [ATLAS].[10].[06Solicitudes] SET idIntermediario = %s, idSolicitante = %s, rlSolicitante = %s, idAprobador = %s, fecInic = %s, fecFin = %s, fecCreacion = %s, idCategLic = %s, idDetalleLic = %s, descripcion = %s WHERE idSolic = %s AND idAprobado = %s",[idResponsablelicedt, idsolicitantelicedt, rlsolicitantelicedt, idAprobador3edt, FecIniclicedt, FecFinlicedt, FecCreacionlicedt, TipLicedt, DetLicedt, DescripLicedt, idsoliclicedt, 1])

                    id_insert_licencia_edt = f"{idsoliclicedt}. {namesoliclicedt}"

                    try:
                        ctx_lic_edt = ClientContext(sharepoint_url_lic_edt).with_user_credentials(username_edt_lic, password_edt_lic)
                        target_folder_url_lic_edt = f"{sharepoint_folder_lic_edt}/Licencias/{id_insert_licencia_edt}"

                        for url in urls_archivos_eliminar_lic:
                            file_to_delete = ctx_lic_edt.web.get_file_by_server_relative_url(url)
                            file_to_delete.delete_object()
                        # ctx_lic.execute_query()

                    except Exception as e:
                        error_message = f"Error al eliminar archivos existentes en SharePoint"
                        messages.error(request, error_message)
                        return redirect('solicitudes')


                    for archivo_nuevo_lic_edt  in archivos_nuevos_lic:

                        try:
                            file_name_lic_edt = archivo_nuevo_lic_edt.name
                            file_extension_lic_edt = file_name_lic_edt.split('.')[-1].lower()

                            if file_extension_lic_edt not in allowed_extensions_lic_edt:
                                error_message = f"El archivo '{file_name_lic_edt}' no tiene una extensión permitida."
                                messages.error(request, error_message)
                                return redirect('solicitudes')
                                    
                            else:
                                file_content_lic_edt = archivo_nuevo_lic_edt.read()

                            try:
                                ctx_lic_edt.web.get_folder_by_server_relative_url(target_folder_url_lic_edt).files.add(file_name_lic_edt, file_content_lic_edt)
                                # target_file_lic_edt = ctx_lic.web.get_folder_by_server_relative_url(target_folder_url_lic_edt).files.add(file_name_lic_edt, file_content_lic_edt)
                                # ctx_lic.load(target_file_lic_edt)
                                # ctx_lic.execute_query()

                            except Exception as e:
                                error_message = f"Error al subir los archivos"
                                messages.error(request, error_message)
                                return redirect('solicitudes')

                        except Exception as e:
                            error_message = f"Error al subir los archivos"
                            messages.error(request, error_message)
                            return redirect('solicitudes')
                        
                    try:
                        ctx_lic_edt.execute_query()  
                        success_message = f"Su solicitud se ha creado correctamente"
                        messages.success(request, success_message)
                        return redirect('solicitudes')

                    except Exception as e:
                        error_message = f"Error al subir los archivos"
                        messages.error(request, error_message)
                        return redirect('solicitudes')

            except (TypeError, DatabaseError) as t:
                error_message = f"Error al editar la solicitud"
                messages.error(request, error_message)

        else:
            error_message = "Ha realizado un metodo de pedido inhabilitado"
            messages.error(request, error_message)
            return redirect('solicitudes')

    else:
        return redirect('error_autenticacion')




#MARK:F.FALTAS
def falta_solicitud (request):      #✓

    if usuario_autenticado(request):

        if request.method == 'POST':
            FecCreacionfal = datetime.date.today()
            idResponsablefal = request.session.get('user_id')
            FecInicfal = request.POST['fecinicfal']
            FecFinfal = request.POST['fecfinfal']
            # Tipfal = request.POST['comfal']
            Detfal = request.POST['causafal']
            Descripfal = request.POST['desfal']
            nameaprobfal = request.POST['aprobadorfal']
            namesolicfal = request.POST['solicitantefal']
            TipoSolicfal = request.POST['tiposolicfal']

            try:
                with connection.cursor() as cursor:

                    idsolicitantefal = cursor.execute("SELECT idRegTrabajador FROM [dbo].[P05RelacLab] WHERE ApellidosNombres = %s AND idVigencia = %s", [namesolicfal, 1]).fetchone()[0]

                    rlsolicitantefal = cursor.execute("SELECT idRegRelacLab FROM [dbo].[P05RelacLab] WHERE ApellidosNombres = %s AND idVigencia = %s", [namesolicfal, 1]).fetchone()[0]
                    
                    idAprobadorfal = cursor.execute("SELECT idRegTrabajador FROM [dbo].[P05RelacLab] WHERE ApellidosNombres = %s AND idVigencia = %s", [nameaprobfal, 1]).fetchone()[0]

                    cursor.execute("INSERT INTO [ATLAS].[10].[06Solicitudes] (idIntermediario, idSolicitante, rlSolicitante, idAprobador, idTipSolic, fecInic, fecFin, fecCreacion, idCausaFalt, descripcion, idAprobado) OUTPUT INSERTED.idSolic VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1)",[idResponsablefal, idsolicitantefal, rlsolicitantefal, idAprobadorfal, TipoSolicfal, FecInicfal, FecFinfal, FecCreacionfal, Detfal, Descripfal])

                    success_message = f"Su solicitud se ha creado correctamente"
                    messages.success(request, success_message)
                    return redirect('solicitudes')

            except TypeError as a:
                error_message = f"Error al crear la solicitud"
                messages.error(request, error_message)

            except DatabaseError as e:
                error_message = f"Error al crear la solicitud"
                messages.error(request, error_message)

        else:
            error_message = "Ha realizado un metodo de pedido inhabilitado"
            messages.error(request, error_message)
            return redirect('solicitudes')

    else:
        return redirect('error_autenticacion')
    



#MARK:F.E.FALTAS
def falta_solicitud_editar (request):   #✓

    if usuario_autenticado(request):

        if request.method == 'POST':
            FecCreacionfaledt = datetime.date.today()
            idResponsablefaledt = request.session.get('user_id')
            FecInicfaledt = request.POST['fecinicfaledt']
            FecFinfaledt = request.POST['fecfinfaledt']
            # Tipfaledt = request.POST['comfaledt']
            Detfaledt = request.POST['causafaledt']
            Descripfaledt = request.POST['desfaledt']
            nameaprobfaledt = request.POST['aprobadorfaledt']
            namesolicfaledt = request.POST['solicitantefaledt']
            idsolicfaledt = request.POST['idsolicfaledt']

            try:
                with connection.cursor() as cursor:

                    idsolicitantefaledt = cursor.execute("SELECT idRegTrabajador FROM [dbo].[P05RelacLab] WHERE ApellidosNombres = %s AND idVigencia = %s", [namesolicfaledt, 1]).fetchone()[0]

                    rlsolicitantefaledt = cursor.execute("SELECT idRegRelacLab FROM [dbo].[P05RelacLab] WHERE ApellidosNombres = %s AND idVigencia = %s", [namesolicfaledt, 1]).fetchone()[0]                    

                    idAprobadorfaledt = cursor.execute("SELECT idRegTrabajador FROM [dbo].[P05RelacLab] WHERE ApellidosNombres = %s AND idVigencia = %s", [nameaprobfaledt, 1]).fetchone()[0]

                    cursor.execute("UPDATE [ATLAS].[10].[06Solicitudes] SET idIntermediario = %s, idSolicitante = %s, rlSolicitante = %s, idAprobador = %s, fecInic = %s, fecFin = %s, fecCreacion = %s, idCausaFalt = %s, descripcion = %s WHERE idSolic = %s AND idAprobado = %s",[idResponsablefaledt, idsolicitantefaledt, rlsolicitantefaledt, idAprobadorfaledt, FecInicfaledt, FecFinfaledt, FecCreacionfaledt, Detfaledt, Descripfaledt, idsolicfaledt, 1])

                    success_message = f"Su solicitud se ha editado correctamente"
                    messages.success(request, success_message)
                    return redirect('solicitudes')

            except TypeError as a:
                error_message = f"Error al editar la solicitud"
                messages.error(request, error_message)

            except DatabaseError as e:
                error_message = f"Error al editar la solicitud"
                messages.error(request, error_message)

        else:
            error_message = "Ha realizado un metodo de pedido inhabilitado"
            messages.error(request, error_message)
            return redirect('solicitudes')

    else:
        return redirect('error_autenticacion')