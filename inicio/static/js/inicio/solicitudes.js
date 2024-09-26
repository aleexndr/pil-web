document.addEventListener("DOMContentLoaded", function() {
    const dateInput = document.querySelectorAll('.flatpickr');

        dateInput.forEach(function(input) {
        flatpickr(input, {
            dateFormat: "Y/m/d"
        });
    });
});


//#region Eliminar Solicitud
document.addEventListener("DOMContentLoaded", function() {
    var closebtn = document.querySelectorAll('.close-card');
    closebtn.forEach(function(button) {
        button.addEventListener('click', function() {
            var solicitudId = this.getAttribute('data-solicitud-id');
            if (confirm("¿Estás seguro de que quieres eliminar esta solicitud?")) {
                var url = eliminarSolicitudUrl.replace('0', solicitudId);
                window.location.href = url;
            }
        });
    });
});




//#region Editar Solicitud
document.addEventListener("DOMContentLoaded", function() {
    var editbtn = document.querySelectorAll('.issued');
    editbtn.forEach(function(button) {
        button.addEventListener('click', function() {
            var solicitudedit = this.getAttribute('data-solicitudedit-id');
            var url = editarSolicitudUrl.replace('0', solicitudedit);
            window.location.href = url;
        });
    });
});




//#region Btn Cerrar y Cancelar
document.addEventListener('DOMContentLoaded', function() {
    var modal = document.getElementById('myModal');
    var modalBtn = document.getElementById('modalBtn');
    var closeButtons = document.querySelectorAll('.close, #close2, #close3, #close4, #close5');
    var vacacionesOption = document.getElementById("vacaciones-form");
    var licenciaOption = document.getElementById("licencia-form");
    var descansoOption = document.getElementById("descanso-form");
    var faltasOption = document.getElementById("faltas-form");
    var selectElement = document.getElementById("miSelect");

    modalBtn.addEventListener('click', function() {
        modal.classList.add('modal');
        modal.classList.remove('hidden');
        vacacionesOption.classList.remove("vacaciones-option"); 
        faltasOption.classList.remove("faltas-option");
        licenciaOption.classList.remove("licencia-option");
        descansoOption.classList.remove("descanso-option");
    });

    closeButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            closeModal();
        });
    });

    function closeModal() {
        modal.classList.remove('modal');
        modal.classList.add('hidden');
        vacacionesOption.classList.add("hidden");
        vacacionesOption.classList.remove('modal');
        descansoOption.classList.add("hidden");
        descansoOption.classList.remove('modal');
        licenciaOption.classList.add("hidden");
        licenciaOption.classList.remove('modal');
        faltasOption.classList.add("hidden");
        faltasOption.classList.remove('modal');
        selectElement.selectedIndex = 0;
    }
});





//#region Leer Archivos Formulario Descanso
let archivosSeleccionadosdes = [];

function handleFileSelectdes() {
    const inputArchivosdes = document.getElementById('archivosdes');
    const nuevosArchivosdes = Array.from(inputArchivosdes.files);

    nuevosArchivosdes.forEach((archivoNuevo) => {
        if (!archivosSeleccionadosdes.some(archivo => archivo.name === archivoNuevo.name && archivo.size === archivoNuevo.size && archivo.lastModified === archivoNuevo.lastModified)) {
            archivosSeleccionadosdes.push(archivoNuevo);
        }
    });

    actualizarListaArchivosdes();
}

function actualizarListaArchivosdes() {
    const archivosSeleccionadosContainerdes = document.getElementById('filenamedes');
    archivosSeleccionadosContainerdes.innerHTML = '';

    archivosSeleccionadosdes.forEach((archivo, index) => {
        const nuevoContenedordes = document.createElement('div');
        nuevoContenedordes.classList.add('file-item');

        const nuevaImagendes = document.createElement('img');
        nuevaImagendes.classList.add('file-icon');
        nuevaImagendes.src = obtenerRutaIcono(archivo.name);

        const nuevoParrafodes = document.createElement('p');
        nuevoParrafodes.textContent = archivo.name;

        const botonEliminardes = document.createElement('span');
        botonEliminardes.classList.add('btn-remove-file');
        botonEliminardes.textContent = '✖';
        botonEliminardes.addEventListener('click', () => {
            eliminarArchivodes(index);
        });

        nuevoContenedordes.appendChild(nuevaImagendes);
        nuevoContenedordes.appendChild(nuevoParrafodes);
        nuevoContenedordes.appendChild(botonEliminardes);
        archivosSeleccionadosContainerdes.appendChild(nuevoContenedordes);
    });

    actualizarInputArchivosdes();
}

function eliminarArchivodes(index) {
    archivosSeleccionadosdes.splice(index, 1);
    actualizarListaArchivosdes();
}

function actualizarInputArchivosdes() {
    const inputArchivosdes = document.getElementById('archivosdes');
    const dataTransferdes = new DataTransfer();

    archivosSeleccionadosdes.forEach(archivo => {
        dataTransferdes.items.add(archivo);
    });

    inputArchivosdes.files = dataTransferdes.files;
}





let archivosSeleccionadosdesedt = [];
let urlsArchivosEliminar = [];

document.addEventListener('DOMContentLoaded', () => {
    const archivosExistentesContainer = document.getElementById('filenamedesedt');
    if (archivosExistentesContainer) {
        const archivosExistentesData = archivosExistentesContainer.getAttribute('data-archivos-existentes');
        if (archivosExistentesData) {
            const archivosExistentes = JSON.parse(archivosExistentesData.replace(/'/g, '"'));
            archivosExistentes.forEach(archivo => {
                archivosSeleccionadosdesedt.push({
                    name: archivo.nombre_archivo,
                    url: archivo.url,
                    existing: true,
                    file: null
                });
            });
            actualizarListaArchivosdesedt();
        }
    }
});


function handleFileSelectdesedt() {
    const inputArchivosdesedt = document.getElementById('archivosdesedt');
    const nuevosArchivosdesedt = Array.from(inputArchivosdesedt.files);

    nuevosArchivosdesedt.forEach((archivoNuevo) => {
        if (!archivosSeleccionadosdesedt.some(archivo => archivo.name === archivoNuevo.name && archivo.size === archivoNuevo.size)) {
            archivosSeleccionadosdesedt.push({
                name: archivoNuevo.name,
                size: archivoNuevo.size,
                existing: false,
                file: archivoNuevo 
            });
        }
    });

    actualizarListaArchivosdesedt();
}

function actualizarListaArchivosdesedt() {
    const archivosSeleccionadosContainerdesedt = document.getElementById('filenamedesedt');
    archivosSeleccionadosContainerdesedt.innerHTML = '';

    archivosSeleccionadosdesedt.forEach((archivo, index) => {
        const nuevoContenedordesedt = document.createElement('div');
        nuevoContenedordesedt.classList.add('file-item');

        const nuevaImagendesedt = document.createElement('img');
        nuevaImagendesedt.classList.add('file-icon');
        nuevaImagendesedt.src = obtenerRutaIcono(archivo.name);

        const nuevoParrafodesedt = document.createElement('p');
        nuevoParrafodesedt.textContent = archivo.name;

        const botonEliminardesedt = document.createElement('span');
        botonEliminardesedt.classList.add('btn-remove-file');
        botonEliminardesedt.textContent = '✖';
        botonEliminardesedt.addEventListener('click', () => {
            eliminarArchivodesedt(index);
        });

        nuevoContenedordesedt.appendChild(nuevaImagendesedt);
        nuevoContenedordesedt.appendChild(nuevoParrafodesedt);
        nuevoContenedordesedt.appendChild(botonEliminardesedt);
        archivosSeleccionadosContainerdesedt.appendChild(nuevoContenedordesedt);
    });

    actualizarInputArchivosdesedt();
}

function eliminarArchivodesedt(index) {
    const archivo = archivosSeleccionadosdesedt[index];
    if (archivo.existing) {
        urlsArchivosEliminar.push(archivo.url);  // Guardar la URL del archivo a eliminar
        console.log(urlsArchivosEliminar)
    }
    archivosSeleccionadosdesedt.splice(index, 1);
    actualizarListaArchivosdesedt();
}

function actualizarInputArchivosdesedt() {
    const inputArchivosdesedt = document.getElementById('archivosdesedt');
    const dataTransferdesedt = new DataTransfer();

    archivosSeleccionadosdesedt.forEach(archivo => {
        if (!archivo.existing && archivo.file) {
            dataTransferdesedt.items.add(archivo.file);
        }
    });

    inputArchivosdesedt.files = dataTransferdesedt.files;

    const inputUrlsEliminar = document.getElementById('urlsArchivosEliminar');
    inputUrlsEliminar.value = JSON.stringify(urlsArchivosEliminar);
}










let archivosSeleccionadoslicedt = [];
let urlsArchivosEliminarlic = [];

document.addEventListener('DOMContentLoaded', () => {
    const archivosExistentesContainerlic = document.getElementById('filenamelicedt');
    if (archivosExistentesContainerlic) {
        const archivosExistentesDatalic = archivosExistentesContainerlic.getAttribute('data-archivos-existentes-lic');
        if (archivosExistentesDatalic) {
            const archivosExistenteslic = JSON.parse(archivosExistentesDatalic.replace(/'/g, '"'));
            archivosExistenteslic.forEach(archivo => {
                archivosSeleccionadoslicedt.push({
                    name: archivo.nombre_archivo,
                    url: archivo.url,
                    existing: true,
                    file: null
                });
            });
            actualizarListaArchivoslicedt();
        }
    }
});


function handleFileSelectlicedt() {
    const inputArchivoslicedt = document.getElementById('archivoslicedt');
    const nuevosArchivoslicedt = Array.from(inputArchivoslicedt.files);

    nuevosArchivoslicedt.forEach((archivoNuevo) => {
        if (!archivosSeleccionadoslicedt.some(archivo => archivo.name === archivoNuevo.name && archivo.size === archivoNuevo.size)) {
            archivosSeleccionadoslicedt.push({
                name: archivoNuevo.name,
                size: archivoNuevo.size,
                existing: false,
                file: archivoNuevo 
            });
        }
    });

    actualizarListaArchivoslicedt();
}

function actualizarListaArchivoslicedt() {
    const archivosSeleccionadosContainerlicedt = document.getElementById('filenamelicedt');
    archivosSeleccionadosContainerlicedt.innerHTML = '';

    archivosSeleccionadoslicedt.forEach((archivo, index) => {
        const nuevoContenedorlicedt = document.createElement('div');
        nuevoContenedorlicedt.classList.add('file-item');

        const nuevaImagenlicedt = document.createElement('img');
        nuevaImagenlicedt.classList.add('file-icon');
        nuevaImagenlicedt.src = obtenerRutaIcono(archivo.name);

        const nuevoParrafolicedt = document.createElement('p');
        nuevoParrafolicedt.textContent = archivo.name;

        const botonEliminarlicedt = document.createElement('span');
        botonEliminarlicedt.classList.add('btn-remove-file');
        botonEliminarlicedt.textContent = '✖';
        botonEliminarlicedt.addEventListener('click', () => {
            eliminarArchivolicedt(index);
        });

        nuevoContenedorlicedt.appendChild(nuevaImagenlicedt);
        nuevoContenedorlicedt.appendChild(nuevoParrafolicedt);
        nuevoContenedorlicedt.appendChild(botonEliminarlicedt);
        archivosSeleccionadosContainerlicedt.appendChild(nuevoContenedorlicedt);
    });

    actualizarInputArchivoslicedt();
}

function eliminarArchivolicedt(index) {
    const archivolic = archivosSeleccionadoslicedt[index];
    if (archivolic.existing) {
        urlsArchivosEliminarlic.push(archivolic.url);
    }
    archivosSeleccionadoslicedt.splice(index, 1);
    actualizarListaArchivoslicedt();
}

function actualizarInputArchivoslicedt() {
    const inputArchivoslicedt = document.getElementById('archivoslicedt');
    const dataTransferlicedt = new DataTransfer();

    archivosSeleccionadoslicedt.forEach(archivo => {
        if (!archivo.existing && archivo.file) {
            dataTransferlicedt.items.add(archivo.file);
        }
    });

    inputArchivoslicedt.files = dataTransferlicedt.files;

    const inputUrlsEliminarlic = document.getElementById('urlsArchivosEliminarlic');
    inputUrlsEliminarlic.value = JSON.stringify(urlsArchivosEliminarlic);
}










//#region Leer Archivos Formulario Licencia
let archivosSeleccionadoslic = [];

function handleFileSelectlic() {
    const inputArchivoslic = document.getElementById('archivoslic');
    const nuevosArchivoslic = Array.from(inputArchivoslic.files);

    nuevosArchivoslic.forEach((archivoNuevo) => {
        if (!archivosSeleccionadoslic.some(archivo => archivo.name === archivoNuevo.name && archivo.size === archivoNuevo.size && archivo.lastModified === archivoNuevo.lastModified)) {
            archivosSeleccionadoslic.push(archivoNuevo);
        }
    });

    actualizarListaArchivoslic();
}

function actualizarListaArchivoslic() {
    const archivosSeleccionadosContainerlic = document.getElementById('filenamelic');
    archivosSeleccionadosContainerlic.innerHTML = '';

    archivosSeleccionadoslic.forEach((archivo, index) => {
        const nuevoContenedorlic = document.createElement('div');
        nuevoContenedorlic.classList.add('file-item');

        const nuevaImagenlic = document.createElement('img');
        nuevaImagenlic.classList.add('file-icon');
        nuevaImagenlic.src = obtenerRutaIcono(archivo.name);

        const nuevoParrafolic = document.createElement('p');
        nuevoParrafolic.textContent = archivo.name;

        const botonEliminarlic = document.createElement('span');
        botonEliminarlic.classList.add('btn-remove-file');
        botonEliminarlic.textContent = '✖';
        botonEliminarlic.addEventListener('click', () => {
            eliminarArchivoslic(index); 
        });

        nuevoContenedorlic.appendChild(nuevaImagenlic);
        nuevoContenedorlic.appendChild(nuevoParrafolic);
        nuevoContenedorlic.appendChild(botonEliminarlic);
        archivosSeleccionadosContainerlic.appendChild(nuevoContenedorlic);
    });

    actualizarInputArchivoslic();
}

function eliminarArchivoslic(index) {
    archivosSeleccionadoslic.splice(index, 1);
    actualizarListaArchivoslic()
}

function actualizarInputArchivoslic() {
    const inputArchivoslic = document.getElementById('archivoslic')
    const dataTransferlic = new DataTransfer();

    archivosSeleccionadoslic.forEach(archivo => {
        dataTransferlic.items.add(archivo);
    })

    inputArchivoslic.files = dataTransferlic.files
}




//#region Mostrar y Ocultar Modelos de Solicitudes
var selectElement = document.getElementById("miSelect");
var vacacionesOption = document.getElementById("vacaciones-form");
var licenciaOption = document.getElementById("licencia-form");
var descansoOption = document.getElementById("descanso-form");
var faltasOption = document.getElementById("faltas-form");                                  // POR MEJORAR

selectElement.addEventListener("change", function() {

    vacacionesOption.classList.add("hidden");
    faltasOption.classList.add("hidden");
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




//#region Opciones de Solicitud Licencia
document.addEventListener('DOMContentLoaded', function() {
    var tipoLicenciaSelect = document.getElementById('typelicense');
    var detalleLicenciaSelect = document.getElementById('licensedetail');

    tipoLicenciaSelect.addEventListener('change', function() {
        var selectedOption = tipoLicenciaSelect.value;
        

        Array.from(detalleLicenciaSelect.options).forEach(function(option) {
            option.classList.add('hidden');
        });

        detalleLicenciaSelect.selectedIndex = 0

        if (selectedOption === '1') {
            
            document.getElementById('maternidad').classList.remove('hidden');
            document.getElementById('paternidad').classList.remove('hidden');
            document.getElementById('familiar').classList.remove('hidden');
            document.getElementById('otros1').classList.remove('hidden');

        } else if (selectedOption === '2') {
            document.getElementById('estudios').classList.remove('hidden');
            document.getElementById('tramites').classList.remove('hidden');
            document.getElementById('personales').classList.remove('hidden');
            document.getElementById('salud').classList.remove('hidden');
            document.getElementById('otros2').classList.remove('hidden');
        }
    });
});

//#region Opciones de Solicitud Licencia (editar)
document.addEventListener('DOMContentLoaded', function() {
    var tipoLicenciaSelectedt = document.getElementById('typelicenseedt');
    var detalleLicenciaSelectedt = document.getElementById('licensedetailedt');

    tipoLicenciaSelectedt.addEventListener('change', function() {
        var selectedOptionedt = tipoLicenciaSelectedt.value;
        

        Array.from(detalleLicenciaSelectedt.options).forEach(function(option) {
            option.classList.add('hidden');
        });

        detalleLicenciaSelectedt.selectedIndex = 0

        if (selectedOptionedt === '1') {

            detalleLicenciaSelectedt.value = '';
            detalleLicenciaSelectedt.selectedIndex = -1;
            
            document.getElementById('maternidadedt').classList.remove('hidden');
            document.getElementById('paternidadedt').classList.remove('hidden');
            document.getElementById('familiaredt').classList.remove('hidden');
            document.getElementById('otros1edt').classList.remove('hidden');

        } else if (selectedOptionedt === '2') {

            detalleLicenciaSelectedt.value = '';
            detalleLicenciaSelectedt.selectedIndex = -1;

            document.getElementById('estudiosedt').classList.remove('hidden');
            document.getElementById('tramitesedt').classList.remove('hidden');
            document.getElementById('personalesedt').classList.remove('hidden');
            document.getElementById('saludedt').classList.remove('hidden');
            document.getElementById('otros2edt').classList.remove('hidden');
        }
    });
});




//#region Obtener ruta Icono
function obtenerRutaIcono(nombreArchivo) {   //LGFM
    var extension = nombreArchivo.split('.').pop().toLowerCase();

    // Puedes agregar más tipos de archivo según sea necesario
    if (extension === 'pdf') {
        return 'https://cdn-icons-png.flaticon.com/128/337/337946.png';
    } else if (extension === 'xlsx' || extension === 'xls' || extension === 'xlsm' || extension === 'xltx' || extension === 'xltm' || extension === 'xlsb' || extension === 'xlam') {
        return 'https://cdn-icons-png.flaticon.com/128/337/337958.png';
    } else if (extension === 'docx' || extension === 'doc' || extension === 'docm' || extension === 'dot' || extension === 'dotx' || extension === 'dotm' || extension === 'docm' || extension === 'application/msword') {
        return 'https://cdn-icons-png.flaticon.com/128/337/337932.png';
    } else if (extension === 'jpg') {
        return 'https://cdn-icons-png.flaticon.com/128/337/337940.png';                          // ESTO ESTA OK
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




//#region Mostrar Lista Solicitudes
document.addEventListener('DOMContentLoaded', function() {

    var vacacionesLink = document.getElementById('link-vacaciones');
    var vacacionesSolicitudes = document.getElementById('solicitudes-vacaciones');
    var descansoLink = document.getElementById('link-descansos');
    var descansoSolicitudes = document.getElementById('solicitudes-descanso');
    var licenciaLink = document.getElementById('link-licencias');
    var licenciaSolicitudes = document.getElementById('solicitudes-licencia');
    var faltasLink = document.getElementById('link-faltas');
    var faltasSolicitudes = document.getElementById('solicitudes-faltas');

    vacacionesLink.addEventListener('click', function() {

        vacacionesLink.classList.add('active-solicitud');
        descansoLink.classList.remove('active-solicitud');
        licenciaLink.classList.remove('active-solicitud');
        faltasLink.classList.remove('active-solicitud');

        vacacionesSolicitudes.classList.remove('hidden');
        descansoSolicitudes.classList.add('hidden');
        licenciaSolicitudes.classList.add('hidden');
        faltasSolicitudes.classList.add('hidden');

    });

    descansoLink.addEventListener('click', function() {

        descansoLink.classList.add('active-solicitud');
        vacacionesLink.classList.remove('active-solicitud');
        licenciaLink.classList.remove('active-solicitud');
        faltasLink.classList.remove('active-solicitud');

        descansoSolicitudes.classList.remove('hidden');
        vacacionesSolicitudes.classList.add('hidden');
        licenciaSolicitudes.classList.add('hidden');
        faltasSolicitudes.classList.add('hidden');

    });

    licenciaLink.addEventListener('click', function() {

        licenciaLink.classList.add('active-solicitud');
        vacacionesLink.classList.remove('active-solicitud');
        descansoLink.classList.remove('active-solicitud');
        faltasLink.classList.remove('active-solicitud');

        licenciaSolicitudes.classList.remove('hidden');
        vacacionesSolicitudes.classList.add('hidden');
        descansoSolicitudes.classList.add('hidden');
        faltasSolicitudes.classList.add('hidden');

    });

    faltasLink.addEventListener('click', function() {

        faltasLink.classList.add('active-solicitud');
        vacacionesLink.classList.remove('active-solicitud');
        descansoLink.classList.remove('active-solicitud');
        licenciaLink.classList.remove('active-solicitud');

        faltasSolicitudes.classList.remove('hidden');
        vacacionesSolicitudes.classList.add('hidden');
        descansoSolicitudes.classList.add('hidden');
        licenciaSolicitudes.classList.add('hidden');

    });

});




//#region Calculo fecha vacaciones
document.addEventListener('DOMContentLoaded', function() {
    var date1Input = document.getElementById('date1');
    var date2Input = document.getElementById('date2');
    var daysInput = document.getElementById('days');

    function calculateDaysvac() {
        var date1 = new Date(date1Input.value);
        var date2 = new Date(date2Input.value);

        if (!date1Input.value || !date2Input.value) {
            daysInput.value = '0 días';
        } else if (isNaN(date1.getTime()) || isNaN(date2.getTime()) || date1 > date2) {
            daysInput.value = 'Invalido';
            daysInput.style.textAlign = 'center';
        } else {
            var timeDifferencevac = Math.abs(date2.getTime() - date1.getTime()) + 1;
            var daysDifferencevac = Math.ceil(timeDifferencevac / (1000 * 3600 * 24));
            daysInput.value = daysDifferencevac + ' días';
            daysInput.style.textAlign = 'left';
        }
    }


    // Calcular los días al cambiar cualquiera de las fechas
    date1Input.addEventListener('input', calculateDaysvac);
    date2Input.addEventListener('input', calculateDaysvac);
});




//#region Calculo fecha vacaciones (editar)
document.addEventListener('DOMContentLoaded', function() {
    var date1Inputedt = document.getElementById('date1edt');
    var date2Inputedt = document.getElementById('date2edt');
    var daysInputedt = document.getElementById('daysedt');

    function calculateDaysedtvac() {
        var date1edt = new Date(date1Inputedt.value);
        var date2edt = new Date(date2Inputedt.value);

        if (!date1Inputedt.value || !date2Inputedt.value) {
            daysInputedt.value = '0 días';
        } else if (isNaN(date1edt.getTime()) || isNaN(date2edt.getTime()) || date1edt > date2edt) {
            daysInputedt.value = 'Invalido';
            daysInputedt.style.textAlign = 'center';
        } else {
            var timeDifferencevacedt = Math.abs(date2edt.getTime() - date1edt.getTime()) + 1;
            var daysDifferencevacedt = Math.ceil(timeDifferencevacedt / (1000 * 3600 * 24));
            daysInputedt.value = daysDifferencevacedt + ' días';
            daysInputedt.style.textAlign = 'left';
        }
    }


    date1Inputedt.addEventListener('input', calculateDaysedtvac);
    date2Inputedt.addEventListener('input', calculateDaysedtvac);

    calculateDaysedtvac();
});




//#region Calculo fecha descansos
document.addEventListener('DOMContentLoaded', function() {
    var date3Input = document.getElementById('date3');
    var date4Input = document.getElementById('date4');
    var days2Input = document.getElementById('days2');

    function calculateDaysdes() {
        var date3 = new Date(date3Input.value);
        var date4 = new Date(date4Input.value);

        if (!date3Input.value || !date4Input.value) {
            days2Input.value = '0 días';
        } else if (isNaN(date3.getTime()) || isNaN(date4.getTime()) || date3 > date4) {
            days2Input.value = 'Invalido';
            days2Input.style.textAlign = 'center';

        } else {
            var time2Differencedes = Math.abs(date4.getTime() - date3.getTime()) + 1;
            var days2Differencedes = Math.ceil(time2Differencedes / (1000 * 3600 * 24));
            days2Input.value = days2Differencedes + ' días';
            days2Input.style.textAlign = 'left';
        }
    }

    // Calcular los días al cambiar cualquiera de las fechas
    date3Input.addEventListener('input', calculateDaysdes);
    date4Input.addEventListener('input', calculateDaysdes);
});




//#region Calculo fecha descansos (editar)
document.addEventListener('DOMContentLoaded', function() {
    var date3Inputedt = document.getElementById('date3edt');
    var date4Inputedt = document.getElementById('date4edt');
    var days2Inputedt = document.getElementById('days2edt');

    function calculateDaysdesedt() {
        var date3edt = new Date(date3Inputedt.value);
        var date4edt = new Date(date4Inputedt.value);

        if (!date3Inputedt.value || !date4Inputedt.value) {
            days2Inputedt.value = '0 días';
        } else if (isNaN(date3edt.getTime()) || isNaN(date4edt.getTime()) || date3edt > date4edt) {
            days2Inputedt.value = 'Invalido';
            days2Inputedt.style.textAlign = 'center';

        } else {
            var time2Differencedesedt = Math.abs(date4edt.getTime() - date3edt.getTime()) + 1;
            var days2Differencedesedt = Math.ceil(time2Differencedesedt / (1000 * 3600 * 24));
            days2Inputedt.value = days2Differencedesedt + ' días';
            days2Inputedt.style.textAlign = 'left';
        }
    }

    // Calcular los días al cambiar cualquiera de las fechas
    date3Inputedt.addEventListener('input', calculateDaysdesedt);
    date4Inputedt.addEventListener('input', calculateDaysdesedt);

    calculateDaysdesedt()
});




//#region Calculo fecha licencias
document.addEventListener('DOMContentLoaded', function() {
    var date5Input = document.getElementById('date5');
    var date6Input = document.getElementById('date6');
    var days3Input = document.getElementById('days3');

    function calculateDayslic() {
        var date5 = new Date(date5Input.value);
        var date6 = new Date(date6Input.value);

        if (!date5Input.value || !date6Input.value) {
            days3Input.value = '0 días';
        } else if (isNaN(date5.getTime()) || isNaN(date6.getTime()) || date5 > date6) {
            days3Input.value = 'Invalido';
            days3Input.style.textAlign = 'center';

        } else {
            var timeDifferencelic = Math.abs(date6.getTime() - date5.getTime()) + 1;
            var daysDifferencelic = Math.ceil(timeDifferencelic / (1000 * 3600 * 24));
            days3Input.value = daysDifferencelic + ' días';
            days3Input.style.textAlign = 'left';
        }
    }

    // Calcular los días al cambiar cualquiera de las fechas
    date5Input.addEventListener('input', calculateDayslic);
    date6Input.addEventListener('input', calculateDayslic);
});




//#region Calculo fecha licencias (editar)
document.addEventListener('DOMContentLoaded', function() {
    var date5Inputedt = document.getElementById('date5edt');
    var date6Inputedt = document.getElementById('date6edt');
    var days3Inputedt = document.getElementById('days3edt');

    function calculateDayslicedt() {
        var date5edt = new Date(date5Inputedt.value);
        var date6edt = new Date(date6Inputedt.value);

        if (!date5Inputedt.value || !date6Inputedt.value) {
            days3Inputedt.value = '0 días';
        } else if (isNaN(date5edt.getTime()) || isNaN(date6edt.getTime()) || date5edt > date6edt) {
            days3Inputedt.value = 'Invalido';
            days3Inputedt.style.textAlign = 'center';

        } else {
            var timeDifferencelicedt = Math.abs(date6edt.getTime() - date5edt.getTime()) + 1;
            var daysDifferencelicedt = Math.ceil(timeDifferencelicedt / (1000 * 3600 * 24));
            days3Inputedt.value = daysDifferencelicedt + ' días';
            days3Inputedt.style.textAlign = 'left';
        }
    }

    // Calcular los días al cambiar cualquiera de las fechas
    date5Inputedt.addEventListener('input', calculateDayslicedt);
    date6Inputedt.addEventListener('input', calculateDayslicedt);

    calculateDayslicedt()
});




//#region Calculo fecha faltas
document.addEventListener('DOMContentLoaded', function() {
    var date7Input = document.getElementById('date7');
    var date8Input = document.getElementById('date8');
    var days4Input = document.getElementById('days4');

    function calculateDaysfal() {
        var date7 = new Date(date7Input.value);
        var date8 = new Date(date8Input.value);

        if (!date7Input.value || !date8Input.value) {
            days4Input.value = '0 días';
        } else if (isNaN(date7.getTime()) || isNaN(date8.getTime()) || date7 > date8) {
            days4Input.value = 'Invalido';
            days4Input.style.textAlign = 'center';

        } else {
            var timeDifferencefal = Math.abs(date8.getTime() - date7.getTime()) + 1;
            var daysDifferencefal = Math.ceil(timeDifferencefal / (1000 * 3600 * 24));
            days4Input.value = daysDifferencefal + ' días';
            days4Input.style.textAlign = 'center';
        }
    }

    // Calcular los días al cambiar cualquiera de las fechas
    date7Input.addEventListener('input', calculateDaysfal);
    date8Input.addEventListener('input', calculateDaysfal);
});




//#region Calculo fecha faltas (editar)
document.addEventListener('DOMContentLoaded', function() {
    var date7Inputedt = document.getElementById('date7edt');
    var date8Inputedt = document.getElementById('date8edt');
    var days4Inputedt = document.getElementById('days4edt');

    function calculateDaysfaledt() {
        var date7edt = new Date(date7Inputedt.value);
        var date8edt = new Date(date8Inputedt.value);

        if (!date7Inputedt.value || !date8Inputedt.value) {
            days4Inputedt.value = '0 días';
        } else if (isNaN(date7edt.getTime()) || isNaN(date8edt.getTime()) || date7edt > date8edt) {
            days4Inputedt.value = 'Invalido';
            days4Inputedt.style.textAlign = 'center';

        } else {
            var timeDifferencefaledt = Math.abs(date8edt.getTime() - date7edt.getTime()) + 1;
            var daysDifferencefaledt = Math.ceil(timeDifferencefaledt / (1000 * 3600 * 24));
            days4Inputedt.value = daysDifferencefaledt + ' días';
            days4Inputedt.style.textAlign = 'left';
        }
    }

    // Calcular los días al cambiar cualquiera de las fechas
    date7Inputedt.addEventListener('input', calculateDaysfaledt);
    date8Inputedt.addEventListener('input', calculateDaysfaledt);

    calculateDaysfaledt()
});




//#region Validacion de formularios
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('creacBtnVacaciones').addEventListener('click', function(event) {
        var formularioValido = validarFormularioVacaciones();

        if (!formularioValido) {
            event.preventDefault();
        } else {
            this.disabled = true;
            this.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Enviando...'
            
            setTimeout(function() {
                var formulariovac = document.getElementById('vacaciones-form');
                formulariovac.submit();
            }, 500);
        }
    });
    
    document.getElementById('crearBtnDescanso').addEventListener('click', function(event) {
        var formularioValido2 = validarFormularioDescanso();

        if(!formularioValido2) {
            event.preventDefault();
        } else {
            this.disabled = true;
            this.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Enviando...'

            setTimeout(function() {
                var formulariodes = document.getElementById('descanso-form');
                formulariodes.submit();
            }, 500);
        }
    })

    document.getElementById('creacBtnLicencia').addEventListener('click', function(event) {
        var formularioValido3 = validarFormularioLicencia();

        if (!formularioValido3) {
            event.preventDefault();
        } else {
            this.disabled = true;
            this.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Enviando...'
            
            setTimeout(function() {
                var formulariolic = document.getElementById('licencia-form');
                formulariolic.submit();
            }, 500);
        }
    });

    document.getElementById('creacBtnFaltas').addEventListener('click', function(event) {
        var formularioValido4 = validarFormularioFaltas();

        if (!formularioValido4) {
            event.preventDefault();
        } else {
            this.disabled = true;
            this.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Enviando...'

            setTimeout(function() {
                var formulariofal = document.getElementById('faltas-form');
                formulariofal.submit();
            }, 500);
        }
    });
})

const editarBtns = document.querySelectorAll('.editar-btn-solicitud');

editarBtns.forEach(function (button) {
    button.addEventListener('click', function (event) {
        event.preventDefault();
        this.disabled = true;
        this.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';

        setTimeout(500);
    });
});




function validarFormularioVacaciones() {
    let date1 = document.getElementById('date1').value;
    let date2 = document.getElementById('date2').value;
    let days = document.getElementById('days').value;
    let authvac = document.getElementById('auth-vacaciones').value;
    let solvac = document.getElementById('solic-vac').value;

    if (!date1 || !date2 || days === 'Invalido' || !authvac || !solvac) {
        alert('Complete todos los campos de manera correcta antes de enviar el formulario');
        return false;
    }

    let nomvalidvac = false;
        let autholistvac = document.querySelectorAll('#solic-autho-vac option');
        autholistvac.forEach(option => {
            if (option.value === authvac) {
                nomvalidvac = true;
            }
        });

        if (!nomvalidvac) {
            alert('El nombre del responsable de autorización no es válido. Seleccione un nombre de la lista.');
            return false;
        }

        return true;
}


function validarFormularioDescanso() {
    let date3 = document.getElementById('date3').value;
    let date4 = document.getElementById('date4').value;
    let days2 = document.getElementById('days2').value;
    let authdes = document.getElementById('auth-descanso').value;
    let soldes = document.getElementById('solic-des').value;
    let archivoInputdes = document.getElementById('archivosdes');
    let archivosSeleccionadosdes = archivoInputdes.files;

    if (!date3 || !date4 || days2 === 'Invalido' || !authdes || !soldes) {
        alert('Complete todos los campos de manera correcta antes de enviar el formulario');
        return false;
    }

    if (archivosSeleccionadosdes.length === 0) {
        alert('Seleccione al menos un archivo antes de enviar el formulario');
        return false;
    }

    if (archivosSeleccionadosdes.length > 4) {
        alert('No puede seleccionar más de 4 archivos.');
        return false;
    }

    let nomvaliddes = false;
        let autholistdes = document.querySelectorAll('#solic-autho-des option');
        autholistdes.forEach(option => {
            if (option.value === authdes) {
                nomvaliddes = true;
            }
        });

        if (!nomvaliddes) {
            alert('El nombre del responsable de autorización no es válido. Seleccione un nombre de la lista.');
            return false;
        }

        return true;
}


function validarFormularioLicencia() {
    let date5 = document.getElementById('date5').value;
    let date6 = document.getElementById('date6').value;
    let days3 = document.getElementById('days3').value;
    let selectlic1 = document.getElementById('typelicense').value;                                              // PARA MEJORAR
    let selectlic2 = document.getElementById('licensedetail').value;
    let textarealic = document.getElementById('textarealic').value;
    let authlic = document.getElementById('auth-license').value;
    let sollic = document.getElementById('solic-lic').value;
    let archivoInputlic = document.getElementById('archivoslic');
    let archivosSeleccionadoslic = archivoInputlic.files;

    if (!date5 || !date6 || days3 === 'Invalido' || !selectlic1 || !selectlic2 || !textarealic || !authlic || !sollic) {
        alert('Complete todos los campos de manera correcta antes de enviar el formulario');
        return false;
    }

    if (archivosSeleccionadoslic.length === 0) {
        alert('Seleccione al menos un archivo antes de enviar el formulario');
        return false;
    }
    
    if (archivosSeleccionadoslic.length > 4) {
        alert('No puede seleccionar más de 4 archivos.');
        return false;
    }

    let nomvalidlic = false;
        let autholistlic = document.querySelectorAll('#solic-autho-lic option');
        autholistlic.forEach(option => {
            if (option.value === authlic) {
                nomvalidlic = true;
            }
        });

        if (!nomvalidlic) {
            alert('El nombre del responsable de autorización no es válido. Seleccione un nombre de la lista.');
            return false;
        }

        return true;
}


function validarFormularioFaltas() {
    let datefal1 = document.getElementById('date7').value;
    let datefal2 = document.getElementById('date8').value;
    let daysfal = document.getElementById('days4').value;
    // let horasfal = document.getElementById('hoursfal').value;
    // let selectfal1 = document.getElementById('comfal').value;
    let selectfal2 = document.getElementById('causafal').value;
    let textareafal = document.getElementById('textareafal').value;
    let authfal = document.getElementById('auth-faltas').value;
    let solfal = document.getElementById('solic-fal').value;

    if (!datefal1 || !datefal2 || daysfal === 'Invalido' || !selectfal1 || !selectfal2 || !textareafal || !authfal || !solfal) {
        alert('Complete todos los campos de manera correcta antes de enviar el formulario');
        return false;
    }

    let nomvalidfal = false;
        let autholistfal = document.querySelectorAll('#solic-autho-fal option');
        autholistfal.forEach(option => {
            if (option.value === authfal) {
                nomvalidfal = true;
            }
        });

        if (!nomvalidfal) {
            alert('El nombre del responsable de autorización no es válido. Seleccione un nombre de la lista.');
            return false;
        }

        return true;
}


function validarFormularioVacacionesedt() {
    let date1edt = document.getElementById('date1edt').value;
    let date2edt = document.getElementById('date2edt').value;
    let daysedt = document.getElementById('daysedt').value;
    let authvacedt = document.getElementById('auth-vacacionesedt').value;
    let solvacedt = document.getElementById('solic-vacedt').value;

    if (!date1edt || !date2edt || daysedt === 'Invalido' || !authvacedt || !solvacedt) {
        alert('Complete todos los campos de manera correcta antes de actualizar el formulario');
        return false;
    }

    let nomvalidvacedt = false;
        let autholistvacedt = document.querySelectorAll('#solic-autho-vac option');
        autholistvacedt.forEach(option => {
            if (option.value === authvacedt) {
                nomvalidvacedt = true;
            }
        });

        if (!nomvalidvacedt) {
            alert('El nombre del responsable de autorización no es válido. Seleccione un nombre de la lista.');
            return false;
        }

        return true;
}


function validarFormularioDescansoedt() {
    let date3edt = document.getElementById('date3edt').value;
    let date4edt = document.getElementById('date4edt').value;
    let days2edt = document.getElementById('days2edt').value;
    let authdesedt = document.getElementById('auth-descansoedt').value;
    let soldesedt = document.getElementById('solic-desedt').value;
    let archivoInputdesedt = document.getElementById('archivosdesedt');
    let archivosSeleccionadosdesedt = archivoInputdesedt.files;

    if (!date3edt || !date4edt || days2edt === 'Invalido' || !authdesedt || !soldesedt) {
        alert('Complete todos los campos de manera correcta antes de actualizar el formulario');
        return false;
    }

    if (archivosSeleccionadosdesedt.length === 0) {
        alert('Seleccione al menos un archivo antes de enviar el formulario');
        return false;
    }

    if (archivosSeleccionadosdesedt.length > 4) {
        alert('No puede seleccionar más de 4 archivos.');
        return false;
    }

    let nomvaliddesedt = false;
        let autholistdesedt = document.querySelectorAll('#solic-autho-des option');
        autholistdesedt.forEach(option => {
            if (option.value === authdesedt) {
                nomvaliddesedt = true;
            }
        });

        if (!nomvaliddesedt) {
            alert('El nombre del responsable de autorización no es válido. Seleccione un nombre de la lista.');
            return false;
        }

        return true;
}


function validarFormularioLicenciaedt() {
    let date5edt = document.getElementById('date5edt').value;
    let date6edt = document.getElementById('date6edt').value;
    let days3edt = document.getElementById('days3edt').value;
    let selectlic1edt = document.getElementById('typelicenseedt').value;                                              // PARA MEJORAR
    let selectlic2edt = document.getElementById('licensedetailedt').value;
    let textarealicedt = document.getElementById('textarealicedt').value;
    let authlicedt = document.getElementById('auth-licenseedt').value;
    let sollicedt = document.getElementById('solic-licedt').value;
    let archivoInputlicedt = document.getElementById('archivoslicedt');
    let archivosSeleccionadoslicedt = archivoInputlicedt.files;

    if (!date5edt || !date6edt || days3edt === 'Invalido' || !selectlic1edt || !selectlic2edt || !textarealicedt || !authlicedt || !sollicedt) {
        alert('Complete todos los campos de manera correcta antes de actualizar el formulario');
        return false;
    }
    
    if (archivosSeleccionadoslicedt.length === 0) {
        alert('Seleccione al menos un archivo antes de enviar el formulario');
        return false;
    }

    if (archivosSeleccionadoslicedt.length > 4) {
        alert('No puede seleccionar más de 4 archivos.');
        return false;
    }

    let nomvalidlicedt = false;
        let autholistlicedt = document.querySelectorAll('#solic-autho-lic option');
        autholistlicedt.forEach(option => {
            if (option.value === authlicedt) {
                nomvalidlicedt = true;
            }
        });

        if (!nomvalidlicedt) {
            alert('El nombre del responsable de autorización no es válido. Seleccione un nombre de la lista.');
            return false;
        }

        return true;
}


function validarFormularioFaltasedt() {
    let datefal1edt = document.getElementById('date7edt').value;
    let datefal2edt = document.getElementById('date8edt').value;
    let daysfaledt = document.getElementById('days4edt').value;
    // let horasfal = document.getElementById('hoursfal').value;
    // let selectfal1edt = document.getElementById('comfaledt').value;
    let selectfal2edt = document.getElementById('causafaledt').value;
    let textareafaledt = document.getElementById('textareafaledt').value;
    let authfaledt = document.getElementById('auth-faltasedt').value;
    let solfaledt = document.getElementById('solic-faledt').value;

    if (!datefal1edt || !datefal2edt || daysfaledt === 'Invalido' || !selectfal2edt || !textareafaledt || !authfaledt || !solfaledt) {
        alert('Complete todos los campos de manera correcta antes de enviar el formulario');
        return false;
    }

    let nomvalidfaledt = false;
        let autholistfaledt = document.querySelectorAll('#solic-autho-fal option');
        autholistfaledt.forEach(option => {
            if (option.value === authfaledt) {
                nomvalidfaledt = true;
            }
        });

        if (!nomvalidfaledt) {
            alert('El nombre del responsable de autorización no es válido. Seleccione un nombre de la lista.');
            return false;
        }

        return true;
}




document.addEventListener('DOMContentLoaded', function() {
    let modaledt = document.getElementById("myModaledt");
    let edtButtons = document.querySelectorAll(".editar-btn");
    let closeBtnedt = document.getElementById("closeedt");
    let closeBtn2edt = document.getElementById("close2edt");
    let closeBtn3edt = document.getElementById("close3edt");
    let closeBtn4edt = document.getElementById("close4edt");
    let closeBtn5edt = document.getElementById("close5edt");
    let edtbtnvac = document.getElementById("editBtnVacaciones");
    let edtbtndes = document.getElementById("editBtnDescanso");
    let edtbtnlic = document.getElementById("editBtnLicencia");
    let edtbtnfal = document.getElementById("editBtnFaltas");

    if (sessionStorage.getItem('modalOpen') === 'true') {
        modaledt.classList.add('modal');
        modaledt.classList.remove('hidden');
    }

    edtButtons.forEach(function(btn) {
        btn.addEventListener('click', function(event) {
            sessionStorage.setItem('modalOpen', 'true');
        });
    });

    closeBtnedt.addEventListener('click', function() {
        closeModaledt();
        sessionStorage.setItem('modalOpen', 'false');
    });

    if (closeBtn2edt) {
        closeBtn2edt.addEventListener('click', function(event) {
            event.preventDefault();
            closeModaledt();
            sessionStorage.setItem('modalOpen', 'false');
        });
    }

    if (closeBtn3edt) {
        closeBtn3edt.addEventListener('click', function(event) {
            event.preventDefault();
            closeModaledt();
            sessionStorage.setItem('modalOpen', 'false');
        });
    }

    if (closeBtn4edt) {
        closeBtn4edt.addEventListener('click', function(event) {
            event.preventDefault();
            closeModaledt();
            sessionStorage.setItem('modalOpen', 'false');
        });
    }

    if (closeBtn5edt) {
        closeBtn5edt.addEventListener('click', function(event) {
            event.preventDefault();
            closeModaledt();
            sessionStorage.setItem('modalOpen', 'false');
        });
    }

    if (edtbtnvac) {
        edtbtnvac.addEventListener('click', function(event) {
            let formularioValidovacedt = validarFormularioVacacionesedt();

            if (!formularioValidovacedt) {
                event.preventDefault();
            } else {
                this.disabled = true;
                this.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Editando...'
                
                setTimeout(function() {
                    let formulariovacedt = document.getElementById('vacaciones-formedt');
                    sessionStorage.setItem('modalOpen', 'false');
                    formulariovacedt.submit();
                }, 500);
            }
        });
    }

    if (edtbtndes) {
        edtbtndes.addEventListener('click', function(event) {
            let formularioValidodesedt = validarFormularioDescansoedt();

            if (!formularioValidodesedt) {
                event.preventDefault();
            } else {
                this.disabled = true;
                this.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Editando...'
                
                setTimeout(function() {
                    let formulariodesedt = document.getElementById('descanso-formedt');
                    sessionStorage.setItem('modalOpen', 'false');
                    formulariodesedt.submit();
                }, 500);
            }
        });
    }

    if (edtbtnlic) {
        edtbtnlic.addEventListener('click', function(event) {
            let formularioValidolicedt = validarFormularioLicenciaedt();

            if (!formularioValidolicedt) {
                event.preventDefault();
            } else {
                this.disabled = true;
                this.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Editando...'
                
                setTimeout(function() {
                    let formulariolicedt = document.getElementById('licencia-formedt');
                    sessionStorage.setItem('modalOpen', 'false');
                    formulariolicedt.submit();
                }, 500);
            }
        });
    }

    if (edtbtnfal) {
        edtbtnfal.addEventListener('click', function(event) {
            let formularioValidofaledt = validarFormularioFaltasedt();

            if (!formularioValidofaledt) {
                event.preventDefault();
            } else {
                this.disabled = true;
                this.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Editando...'
                
                setTimeout(function() {
                    let formulariofaledt = document.getElementById('faltas-formedt');
                    sessionStorage.setItem('modalOpen', 'false');
                    formulariofaledt.submit();
                }, 500);
            }
        });
    }

    function closeModaledt() {
        modaledt.classList.remove('modal');
        modaledt.classList.add('hidden');
    }
});




document.addEventListener('DOMContentLoaded', function() {
    // Obtener los elementos de los enlaces de tipo de solicitudes
    const vacacionesLink = document.getElementById('link-vacaciones');
    const descansosLink = document.getElementById('link-descansos');
    const licenciasLink = document.getElementById('link-licencias');
    const faltasLink = document.getElementById('link-faltas');

    // Obtener los contenedores de las solicitudes
    const solicitudesVacaciones = document.getElementById('solicitudes-vacaciones');
    const solicitudesDescansos = document.getElementById('solicitudes-descanso');
    const solicitudesLicencias = document.getElementById('solicitudes-licencia');
    const solicitudesFaltas = document.getElementById('solicitudes-faltas');

    // Obtener el tipo de solicitud seleccionado desde localStorage
    const selectedRequestType = localStorage.getItem('selectedRequestType') || 'vacaciones';

    // Función para activar un tipo de solicitud
    function activarSolicitud(type) {
        // Remover la clase "active-solicitud" de todos los enlaces
        vacacionesLink.classList.remove('active-solicitud');
        descansosLink.classList.remove('active-solicitud');
        licenciasLink.classList.remove('active-solicitud');
        faltasLink.classList.remove('active-solicitud');

        // Agregar la clase "hidden" a todos los contenedores
        solicitudesVacaciones.classList.add('hidden');
        solicitudesDescansos.classList.add('hidden');
        solicitudesLicencias.classList.add('hidden');
        solicitudesFaltas.classList.add('hidden');

        // Activar el tipo de solicitud correspondiente
        if (type === 'vacaciones') {
            vacacionesLink.classList.add('active-solicitud');
            solicitudesVacaciones.classList.remove('hidden');
        } else if (type === 'descansos') {
            descansosLink.classList.add('active-solicitud');
            solicitudesDescansos.classList.remove('hidden');
        } else if (type === 'licencias') {
            licenciasLink.classList.add('active-solicitud');
            solicitudesLicencias.classList.remove('hidden');
        } else if (type === 'faltas') {
            faltasLink.classList.add('active-solicitud');
            solicitudesFaltas.classList.remove('hidden');
        }

        // Guardar la selección en localStorage
        localStorage.setItem('selectedRequestType', type);
    }

    // Asignar los eventos de click a los enlaces
    vacacionesLink.addEventListener('click', function() {
        activarSolicitud('vacaciones');
    });

    descansosLink.addEventListener('click', function() {
        activarSolicitud('descansos');
    });

    licenciasLink.addEventListener('click', function() {
        activarSolicitud('licencias');
    });

    faltasLink.addEventListener('click', function() {
        activarSolicitud('faltas');
    });

    // Activar la solicitud seleccionada o la predeterminada (vacaciones)
    activarSolicitud(selectedRequestType);
});
