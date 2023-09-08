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
    event.preventDefault();
  
    const selectedId = document.getElementById('selected-id').value;
    const passwordField = document.getElementById('password-valid').value;
  
    const errorMessage = document.getElementById('error-message');
    if (errorMessage) {
      errorMessage.remove();
    }


  fetch(`/check-password/?id=${selectedId}&password=${encodeURIComponent(passwordField)}`)
  .then(response => response.json())
  .then(data => {
    const errorMessageDiv = document.querySelector('#error-message');

    if (data.password_match) {
      window.location.href = '/index';
    } else {
      // Contraseña incorrecta, muestra el mensaje de error arriba del botón
      const newErrorMessage = document.createElement('div');
      newErrorMessage.id = 'error-message';
      newErrorMessage.className = 'alert-custom';
      newErrorMessage.innerHTML = '<ul><li>El usuario o contraseña son incorrectos. Por favor, inténtelo de nuevo.</li></ul>';
      
      // Inserta el mensaje de error antes del botón de inicio de sesión
      const botonLoginDiv = document.querySelector('.boton-login-div');
      botonLoginDiv.parentNode.insertBefore(newErrorMessage, botonLoginDiv);
    }
  })
  .catch(error => {
    console.error('Error en la solicitud:', error);
  });

  });  
});
