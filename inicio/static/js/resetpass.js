document.addEventListener("DOMContentLoaded", function() {

  const fechaInput = document.getElementById("date");

  flatpickr(fechaInput, {
    dateFormat: "Y/m/d",
    placeholder: "Fecha de Nacimiento",
  });
});