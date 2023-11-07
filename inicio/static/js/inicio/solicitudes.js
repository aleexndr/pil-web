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



document.addEventListener('DOMContentLoaded', function() {
    var modal = document.getElementById('myModal');
    var modalBtn = document.querySelector('.button-create');
    var closeBtn = document.querySelector('.close');
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
});



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



document.addEventListener('DOMContentLoaded', function() {
    var tipoLicenciaSelect = document.getElementById('typelicense');
    var detalleLicenciaSelect = document.getElementById('licensedetail');

    tipoLicenciaSelect.addEventListener('change', function() {
        var selectedOption = tipoLicenciaSelect.value;

        // Oculta todas las opciones por defecto
        Array.from(detalleLicenciaSelect.options).forEach(function(option) {
            option.classList.add('hidden');
        });

        // Muestra las opciones según la selección del primer select
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


