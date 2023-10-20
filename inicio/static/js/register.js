document.addEventListener("DOMContentLoaded", function() {

    const fechaInput = document.getElementById("date");

    flatpickr(fechaInput, {
      dateFormat: "Y/m/d",
      placeholder: "Fecha de Nacimiento",
    });
});

document.getElementById('dni').addEventListener('input', function() {
  const documentoValue = this.value;
  const usernameField = document.getElementById('username');

  usernameField.value = documentoValue;
})