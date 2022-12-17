function sendEmail() {
    var name = document.getElementById('name').value;
    var email = document.getElementById('email').value;
    var phone = document.getElementById('phone').value;
    var subject = document.getElementById('subject').value;
    var message = document.getElementById('message').value;
  //  var body = 'Nombre: ' + name + 'nEmail: ' + email + 'nTeléfono: ' + phone + 'nMensaje: ' + message;
    if (name == "") {
      alert("Por favor ingresa tu nombre");
      return false;
    } else if (email == "") {
      alert("Por favor ingresa tu correo electrónico");
      return false;
    }else if (phone == "") {
      alert("Por favor ingresa tu número de teléfono");
      return false;
    }else if (subject == "") {
      alert("Por favor ingresa el asunto");
      return false;
    }else if (message == "") {
      alert("Por favor ingresa tu mensaje");
      return false;
    }else {alert("Mensaje enviado. ¡Gracias por contactarnos!");
    return true;}
  }
  
enviar.addEventListener("click", sendEmail);