// alert('hola probando')

document.addEventListener('DOMContentLoaded', function() {
  const searchInput = document.getElementById('search-input');
  const searchResultsList = document.getElementById('search-results-list');

  searchInput.addEventListener('input', function() {
    const searchTerm = searchInput.value.trim();

    if (searchTerm === '') {
      searchResultsList.innerHTML = '';
      return;
    }

    fetch(`/search/?q=${encodeURIComponent(searchTerm)}`)
      .then(response => response.json())
      .then(data => {
        searchResultsList.innerHTML = '';

        for (let i = 0; i < data.results.length; i++) {
          const result = data.results[i];
          const li = document.createElement('li');
          li.textContent = result;
          li.addEventListener('click', function() {
            searchInput.value = result;
            var index = i
            document.getElementById("selected-id").value = data.ids[index];
            console.log("Valor de selected_id:", data.ids[i]);
            searchResultsList.innerHTML = '';
          });          
          searchResultsList.appendChild(li);
        }
      })
      .catch(error => {
        console.error('Error en la solicitud:', error);
      });
  });

  const submitButton = document.getElementById('submit-button');
  submitButton.addEventListener('click', function(event) {
    event.preventDefault(); // Evita que el formulario se envíe automáticamente
  
    const selectedId = document.getElementById('selected-id').value;
    const passwordField = document.getElementById('password-valid').value;
  
    // Verifica si el elemento "error-message" existe antes de intentar eliminarlo
    const errorMessage = document.getElementById('error-message');
    if (errorMessage) {
      errorMessage.remove(); // Elimina mensajes de error anteriores
    }
  
    // Realiza una solicitud AJAX para verificar la contraseña
    fetch(`/check-password/?id=${selectedId}&password=${encodeURIComponent(passwordField)}`)
      .then(response => response.json())
      .then(data => {
        if (data.password_match) {
          // Contraseña correcta, redirige a index.html
          window.location.href = '/index'; // Redirige al usuario a index.html
        } else {
          // Contraseña incorrecta, muestra un mensaje de error
          const newErrorMessage = document.createElement('div');
          newErrorMessage.id = 'error-message';
          newErrorMessage.className = 'alert-custom';
          newErrorMessage.innerHTML = '<ul><li>La contraseña ingresada es incorrecta.</li></ul>';
          document.querySelector('form').appendChild(newErrorMessage);
        }
      })
      .catch(error => {
        console.error('Error en la solicitud:', error);
      });
  });  
});
