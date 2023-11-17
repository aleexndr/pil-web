// ***** CALENDARIOS PARA ESCOJER FECHAS *****
document.addEventListener("DOMContentLoaded", function() {

    const fechaInput1 = document.getElementById("date1");
    const fechaInput2 = document.getElementById("date2");
    const fechaInput3 = document.getElementById("date3");
    const fechaInput4 = document.getElementById("date4");
    const fechaInput5 = document.getElementById("date5");
    const fechaInput6 = document.getElementById("date6");
    const fechaInput7 = document.getElementById("date7");
    const fechaInput8 = document.getElementById("date8");

    flatpickr(fechaInput1, {
      dateFormat: "Y/m/d",
      placeholder: "Fecha de Nacimiento",
    });
    flatpickr(fechaInput2, {
        dateFormat: "Y/m/d",
        placeholder: "Fecha de Nacimiento",
    });
    flatpickr(fechaInput3, {
        dateFormat: "Y/m/d",
        placeholder: "Fecha de Nacimiento",
    });
    flatpickr(fechaInput4, {
        dateFormat: "Y/m/d",
        placeholder: "Fecha de Nacimiento",
    });
    flatpickr(fechaInput5, {
        dateFormat: "Y/m/d",
        placeholder: "Fecha de Nacimiento",
    });
    flatpickr(fechaInput6, {
        dateFormat: "Y/m/d",
        placeholder: "Fecha de Nacimiento",
    });
    flatpickr(fechaInput7, {
        dateFormat: "Y/m/d",
        placeholder: "Fecha de Nacimiento",
    });
    flatpickr(fechaInput8, {
        dateFormat: "Y/m/d",
        placeholder: "Fecha de Nacimiento",
    });
});




// ***** BOTON DE CERRAR Y DE CANCELAR *****
document.addEventListener('DOMContentLoaded', function() {
    var modal = document.getElementById('myModal');
    var modalBtn = document.querySelector('.button-create');
    var closeBtn = document.getElementById("close");
    var closeBtn2 = document.getElementById("close2");
    var closeBtn3 = document.getElementById("close3");
    var closeBtn4 = document.getElementById("close4");
    var vacacionesOption = document.querySelector(".vacaciones-option");
    var licenciaOption = document.querySelector(".licencia-option");
    var descansoOption = document.querySelector(".descanso-option");
    var faltasOption = document.querySelector(".faltas-option");
    var selectElement = document.getElementById("miSelect");

    modalBtn.addEventListener('click', function() {
        modal.classList.add('modal');
        modal.classList.remove('hidden');
        vacacionesOption.classList.remove("vacaciones-option");
        faltasOption.classList.remove("faltas-option");
        licenciaOption.classList.remove("licencia-option");
        descansoOption.classList.remove("descanso-option");

    });

    closeBtn.addEventListener('click', function() {
        modal.classList.remove('modal');
        modal.classList.add('hidden');
        vacacionesOption.classList.add("hidden");
        faltasOption.classList.add("hidden");
        licenciaOption.classList.add("hidden");
        descansoOption.classList.add("hidden");
        selectElement.selectedIndex = "";
    });

    closeBtn2.addEventListener('click', function() {
        modal.classList.remove('modal');
        modal.classList.add('hidden');
        vacacionesOption.classList.add("hidden");
        faltasOption.classList.add("hidden");
        licenciaOption.classList.add("hidden");
        descansoOption.classList.add("hidden");
        selectElement.selectedIndex = "";
    });

    closeBtn3.addEventListener('click', function() {
        modal.classList.remove('modal');
        modal.classList.add('hidden');
        vacacionesOption.classList.add("hidden");
        faltasOption.classList.add("hidden");
        licenciaOption.classList.add("hidden");
        descansoOption.classList.add("hidden");
        selectElement.selectedIndex = "";
    });

    closeBtn4.addEventListener('click', function() {
        modal.classList.remove('modal');
        modal.classList.add('hidden');
        vacacionesOption.classList.add("hidden");
        faltasOption.classList.add("hidden");
        licenciaOption.classList.add("hidden");
        descansoOption.classList.add("hidden");
        selectElement.selectedIndex = "";
    });
});




// ***** MOSTRAR Y OCULTAR MODELOS DE SOLICITUDES *****
var selectElement = document.getElementById("miSelect");
var vacacionesOption = document.querySelector(".vacaciones-option");
var licenciaOption = document.querySelector(".licencia-option");
var descansoOption = document.querySelector(".descanso-option");
var faltasOption = document.querySelector(".faltas-option");

selectElement.addEventListener("change", function() {
    
    vacacionesOption.classList.add("hidden");
    faltasOption.classList.add("hidden")
    licenciaOption.classList.add("hidden");
    descansoOption.classList.add("hidden");

    if (selectElement.value !== "") {
        if (selectElement.value === "vacaciones") {
            vacacionesOption.classList.remove("hidden");
            vacacionesOption.classList.add("vacaciones-option");
            faltasOption.classList.remove("faltas-option");
            faltasOption.classList.add("hidden");
            licenciaOption.classList.remove("licencia-option");
            licenciaOption.classList.add("hidden")
            descansoOption.classList.remove("descanso-option")
            descansoOption.classList.add("hidden")

        } else if (selectElement.value === "faltas") {
            faltasOption.classList.remove("hidden")
            faltasOption.classList.add("faltas-option")
            licenciaOption.classList.remove("licencia-option");
            licenciaOption.classList.add("hidden");
            vacacionesOption.classList.remove("vacaciones-option");
            vacacionesOption.classList.add("hidden")
            descansoOption.classList.remove("descanso-option")
            descansoOption.classList.add("hidden")
    
        } else if (selectElement.value === "licencia") {
            licenciaOption.classList.remove("hidden");
            licenciaOption.classList.add("licencia-option");
            faltasOption.classList.remove("faltas-option");
            faltasOption.classList.add("hidden");
            vacacionesOption.classList.remove("vacaciones-option");
            vacacionesOption.classList.add("hidden")
            descansoOption.classList.remove("descanso-option")
            descansoOption.classList.add("hidden")
    
        } else if (selectElement.value === "descanso") {
            descansoOption.classList.remove("hidden")
            descansoOption.classList.add("descanso-option")
            faltasOption.classList.remove("faltas-option");
            faltasOption.classList.add("hidden");
            licenciaOption.classList.remove("licencia-option");
            licenciaOption.classList.add("hidden");
            vacacionesOption.classList.remove("vacaciones-option");
            vacacionesOption.classList.add("hidden")
        }
    }
});




// ***** OPCIONES DE SOLICITUD DE LICENCIA *****
document.addEventListener('DOMContentLoaded', function() {
    var tipoLicenciaSelect = document.getElementById('typelicense');
    var detalleLicenciaSelect = document.getElementById('licensedetail');

    tipoLicenciaSelect.addEventListener('change', function() {
        var selectedOption = tipoLicenciaSelect.value;
        

        Array.from(detalleLicenciaSelect.options).forEach(function(option) {
            option.classList.add('hidden');
        });

        detalleLicenciaSelect.selectedIndex = 0

        if (selectedOption === 'con') {
            
            document.getElementById('maternidad').classList.remove('hidden');
            document.getElementById('paternidad').classList.remove('hidden');
            document.getElementById('familiar').classList.remove('hidden');
            document.getElementById('otros1').classList.remove('hidden');

        } else if (selectedOption === 'sin') {
            document.getElementById('estudios').classList.remove('hidden');
            document.getElementById('tramites').classList.remove('hidden');
            document.getElementById('personales').classList.remove('hidden');
            document.getElementById('salud').classList.remove('hidden');
            document.getElementById('otros2').classList.remove('hidden');
        }
    });
});




// ***** LEER ARCHIVOS *****
var archivosSeleccionados = [];

function handleFileSelect() {
    var inputArchivos = document.getElementById('archivo');
    archivosSeleccionados = archivosSeleccionados.concat(Array.from(inputArchivos.files));
    actualizarListaArchivos();
}

function actualizarListaArchivos() {
    var archivosSeleccionadosContainer = document.getElementById('filename');
    archivosSeleccionadosContainer.innerHTML = '';

    archivosSeleccionados.forEach(function(archivo) {
        var nuevoContenedor = document.createElement('div');
        nuevoContenedor.classList.add('file-item');

        var nuevaImagen = document.createElement('img');
        nuevaImagen.classList.add('file-icon');
        nuevaImagen.src = obtenerRutaIcono(archivo.name);

        var nuevoParrafo = document.createElement('p');
        nuevoParrafo.textContent = archivo.name;

        var botonEliminar = document.createElement('span');
        botonEliminar.classList.add('btn-remove-file');
        botonEliminar.textContent = '✖';
        botonEliminar.addEventListener('click', function() {
            archivosSeleccionados = archivosSeleccionados.filter(function(arch) {
                return arch !== archivo;
            });
            actualizarListaArchivos();
        });

        nuevoContenedor.appendChild(nuevaImagen);
        nuevoContenedor.appendChild(nuevoParrafo);
        nuevoContenedor.appendChild(botonEliminar);
        archivosSeleccionadosContainer.appendChild(nuevoContenedor);
    });
}

function enviarFormulario() {
    subirArchivosPorSeparado();
}

function subirArchivosPorSeparado() {
    var csrftoken = getCookie('csrftoken');

    archivosSeleccionados.forEach(function(archivo) {
        var formData = new FormData();
        formData.append('archivo', archivo);

        fetch(subirArchivoUrl, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrftoken
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error al subir el archivo ${archivo.name}`);
            }
            return response.text();
        })
        .then(data => {
            console.log(data);
        })
        .catch(error => {
            console.error(error);
        });
    });

    archivosSeleccionados = [];
    actualizarListaArchivos();
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function obtenerRutaIcono(nombreArchivo) {
    return 'ruta_del_icono/' + nombreArchivo;
}




// ***** OBTENER TIPO DE ARCHIVO *****
function obtenerRutaIcono(nombreArchivo) {
    var extension = nombreArchivo.split('.').pop().toLowerCase();

    // Puedes agregar más tipos de archivo según sea necesario
    if (extension === 'pdf') {
        return 'https://cdn-icons-png.flaticon.com/128/337/337946.png';
    } else if (extension === 'xlsx' || extension === 'xls' || extension === 'xlsm' || extension === 'xltx' || extension === 'xltm' || extension === 'xlsb' || extension === 'xlam') {
        return 'https://cdn-icons-png.flaticon.com/128/337/337958.png';
    } else if (extension === 'docx' || extension === 'doc' || extension === 'docm' || extension === 'dot' || extension === 'dotx' || extension === 'dotm' || extension === 'docm' || extension === 'application/msword') {
        return 'https://cdn-icons-png.flaticon.com/128/337/337932.png';
    } else if (extension === 'jpg') {
        return 'https://cdn-icons-png.flaticon.com/128/337/337940.png';
    } else if (extension === 'png') {
        return 'https://cdn-icons-png.flaticon.com/128/337/337948.png';
    } else if (extension === 'gif') {
        return 'https://cdn-icons-png.flaticon.com/128/337/337936.png';
    } else if (extension === 'jpeg' || extension === 'webp' || extension === 'jfif') {
        return 'https://cdn-icons-png.flaticon.com/128/3342/3342137.png';
    } else {
        return 'https://cdn-icons-png.flaticon.com/128/8304/8304503.png';
    }
}




// ***** FILTRO DE VISTAS DE SOLICITUDES *****
document.addEventListener('DOMContentLoaded', function() {

    var vacacionesLink = document.getElementById('link-vacaciones');
    var vacacionesSolicitudes = document.getElementById('solicitudes-vacaciones');
    var descansoLink = document.getElementById('link-descansos');
    var descansoSolicitudes = document.getElementById('solicitudes-descanso');
    var licenciaLink = document.getElementById('link-licencias');
    var licenciaSolicitudes = document.getElementById('solicitudes-licencia');

    vacacionesLink.addEventListener('click', function() {

        vacacionesLink.classList.add('active-solicitud')
        descansoLink.classList.remove('active-solicitud')
        licenciaLink.classList.remove('active-solicitud')

        vacacionesSolicitudes.classList.remove('hidden');
        descansoSolicitudes.classList.add('hidden');
        licenciaSolicitudes.classList.add('hidden');

    });

    descansoLink.addEventListener('click', function() {

        descansoLink.classList.add('active-solicitud')
        vacacionesLink.classList.remove('active-solicitud')
        licenciaLink.classList.remove('active-solicitud')

        descansoSolicitudes.classList.remove('hidden');
        vacacionesSolicitudes.classList.add('hidden');
        licenciaSolicitudes.classList.add('hidden');

    });

    licenciaLink.addEventListener('click', function() {

        licenciaLink.classList.add('active-solicitud')
        vacacionesLink.classList.remove('active-solicitud')
        descansoLink.classList.remove('active-solicitud')

        licenciaSolicitudes.classList.remove('hidden');
        vacacionesSolicitudes.classList.add('hidden');
        descansoSolicitudes.classList.add('hidden');

    });

});




// ***** CANTIDAD DE DIAS ENTRE F.INICIO Y F.FIN *****


// *** CALCULO DE FECHAS DE VACACIONES ***
document.addEventListener('DOMContentLoaded', function() {
    var date1Input = document.getElementById('date1');
    var date2Input = document.getElementById('date2');
    var daysInput = document.getElementById('days');

    function calculateDays() {
        var date1 = new Date(date1Input.value);
        var date2 = new Date(date2Input.value);

        if (!date1Input.value || !date2Input.value) {
            daysInput.value = '0 días';
        } else if (isNaN(date1.getTime()) || isNaN(date2.getTime()) || date1 > date2) {
            daysInput.value = 'Invalido';
            daysInput.style.textAlign = 'center';
        } else {
            var timeDifference = (Math.abs(date2.getTime() - date1.getTime())) + 1;
            var daysDifference = Math.ceil(timeDifference / (1000 * 3600 * 24));
            daysInput.value = daysDifference + ' días';
            daysInput.style.textAlign = 'left';
        }
    }

    // Calcular los días al cambiar cualquiera de las fechas
    date1Input.addEventListener('input', calculateDays);
    date2Input.addEventListener('input', calculateDays);
});


// *** CALCULO DE FECHAS DE DESCANSO ***
document.addEventListener('DOMContentLoaded', function() {
    var date3Input = document.getElementById('date3');
    var date4Input = document.getElementById('date4');
    var days2Input = document.getElementById('days2');

    function calculateDays() {
        var date3 = new Date(date3Input.value);
        var date4 = new Date(date4Input.value);

        if (!date3Input.value || !date4Input.value) {
            days2Input.value = '0 días';
        } else if (isNaN(date3.getTime()) || isNaN(date4.getTime()) || date3 > date4) {
            days2Input.value = 'Invalido';
            days2Input.style.textAlign = 'center';

        } else {
            var timeDifference = Math.abs(date4.getTime() - date3.getTime());
            var daysDifference = Math.ceil(timeDifference / (1000 * 3600 * 24));
            days2Input.value = daysDifference + ' días';
            days2Input.style.textAlign = 'left';
        }
    }

    // Calcular los días al cambiar cualquiera de las fechas
    date3Input.addEventListener('input', calculateDays);
    date4Input.addEventListener('input', calculateDays);
});


// *** CALCULO DE FECHAS DE LICENCIA ***
document.addEventListener('DOMContentLoaded', function() {
    var date5Input = document.getElementById('date5');
    var date6Input = document.getElementById('date6');
    var days3Input = document.getElementById('days3');

    function calculateDays() {
        var date5 = new Date(date5Input.value);
        var date6 = new Date(date6Input.value);

        if (!date5Input.value || !date6Input.value) {
            days3Input.value = '0 días';
        } else if (isNaN(date5.getTime()) || isNaN(date6.getTime()) || date5 > date6) {
            days3Input.value = 'Invalido';
            days3Input.style.textAlign = 'center';

        } else {
            var timeDifference = Math.abs(date6.getTime() - date5.getTime());
            var daysDifference = Math.ceil(timeDifference / (1000 * 3600 * 24));
            days3Input.value = daysDifference + ' días';
            days3Input.style.textAlign = 'left';
        }
    }

    // Calcular los días al cambiar cualquiera de las fechas
    date5Input.addEventListener('input', calculateDays);
    date6Input.addEventListener('input', calculateDays);
});



//***** VALIDAR FORMULARIO DE VACACIONES *****
function validarFormularioVacaciones() {
    var date1 = document.getElementById('date1').value;
    var date2 = document.getElementById('date1').value;
    var days = document.getElementById('days').value
    var auth = document.getElementById('auth-vacaciones').value;
    var checkbox = document.getElementById('check-vacaciones').checked;

    if (!date1 || !date2 || days === 'Invalido' || !auth || !checkbox) {
        alert('Complete todos los campos de manera correcta antes de enviar el formulario');
        return false;
    }

    return true
}