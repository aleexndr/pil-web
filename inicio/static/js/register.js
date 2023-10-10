document.addEventListener("DOMContentLoaded", function() {

    const fechaInput = document.getElementById("date");

    flatpickr(fechaInput, {
      dateFormat: "d/m/Y",
      placeholder: "Fecha de Nacimiento",
      });
    });