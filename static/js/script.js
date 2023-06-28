function mostrarFormulario(){
    document.getElementById('form_post_admin').style.display='block';
}
function crearComentarios(){
    document.getElementById('form_comentarios').style.display='block';
}

document.addEventListener("DOMContentLoaded", function() {
    // Obtener mensajes existentes
    fetch('/messages')
      .then(response => response.json())
      .then(data => {
        data.forEach(message => {
          const messageElement = document.createElement('p');
          messageElement.textContent = message.text;
          document.getElementById('message-container').appendChild(messageElement);
        });
      });

    // Enviar mensaje
    document.getElementById('message-form').addEventListener('submit', function(event) {
      event.preventDefault();
      const message = document.getElementById('message-input').value;
      const user = document.getElementById('user-input').value;

      fetch('/messages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: message, user: user })
      })
        .then(response => response.json())
        .then(data => {
          const messageElement = document.createElement('p');
          messageElement.textContent = message;
          document.getElementById('message-container').appendChild(messageElement);
          document.getElementById('message-input').value = '';
          document.getElementById('user-input').value = '';
        });
    });
  });





