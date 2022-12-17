//Variables globales
var id = 0; //Variable para guardar el id de la pregunta
var random = 0; //Variable para seleccionar examen aleatorio
var examenSelect = null; //Variable para guardar el examen seleccionado

//Variables para guardar las respuestas de la preguntas
var respuestasOrdenadas = []; //Variable para guardar las respuestas ordenadas
var respuestasCorrectas = []; //Variable para guardar las respuestas correctas
var preguntasObtenidas = false; //Variable para saber si se han obtenido las preguntas y no volver a generar otro examen
var preguntas; //Variable para guardar las preguntas del examen seleccionado

var checkMarcado = []; /*Variable array que contiene si en las posion del array ha sido seleccinado algun radioButton, 
las respuestas del usuario que ha marcado y la posicion de la pregunta*/

var examenTerminado = false; //Variable para saber si el examen ha terminado

//Variables para guardar los datos del examen
var miform = document.getElementById("form"); //Variable para obtener datos del formulario
var csrftoken = miform.querySelector("[name=csrfmiddlewaretoken]").value; //Variable para guardar el token csrf

const URLAPI = "http://autoescuelalupita.pythonanywhere.com/";

//Alerta para que no se cierre la pagina sin guardar
window.addEventListener("beforeunload", function (event) {
  // Muestra una alerta al usuario
  event.preventDefault();
  alert(
    "¡Cuidado! Si cierras o actualizas la página perderás todos los cambios no guardados."
  );
});

//Carga funcion que se lanza al cargar la pagina
window.addEventListener("load", async () => {
  await cargaInicial();
});

//Carga inicial
const cargaInicial = async () => {
  inicarTemporizador();
  await mostrarPregunta(id);
  await enumPreguntas();
 
};

//Funcion para iniciar el temporizador
function inicarTemporizador() {
  let tiempoRestante = 30 * 60; // 30 minutos en segundos
  let temporizador = setInterval(() => {
    tiempoRestante--;
    let minutos = Math.floor(tiempoRestante / 60);
    let segundos = tiempoRestante % 60;
    if (minutos < 10) {
      minutos = "0" + minutos;
    } else if (segundos < 10) {
      segundos = "0" + segundos;
    };
    if (tiempoRestante == 0) {
      clearInterval(temporizador);
      alert("Se ha acabado el tiempo");
    };
    document.getElementById("temporizador").innerHTML = `${minutos}:${segundos}`;
  }, 1000);
}
//Funcion para seleccionar el examen aleatorio
const selecionarExamen = async () => {
  try {
    const res = await fetch(URLAPI+"api/examen/");
    const data = await res.json();
    random = Math.floor(Math.random() * data.length);

    if (data) {
      examenSelect = data[random];
      return examenSelect;
    } else {
      return console.log(error);
    }
  } catch (error) {
    console.log(error);
  }
};

//Funcion para obtener las preguntas del examen seleccionado y reordenar las respuestas posicionandolas aleatoriamente
const obtenerPreguntas = async () => {
  try {
    const res = await fetch(URLAPI+"api/pregunta/");
    const data = await res.json();

    if (data) {
      const preguntasJson = data;
      const examenSelect = await selecionarExamen();
      let preguntas = [];
      preguntasJson.forEach((pregunta) => {
        examenSelect.preguntas.forEach((e) => {
          if (e == pregunta.id_Pregunta) {
            preguntas.push(pregunta);
            const respuestas = [
              pregunta.respuesta_Falsa_1,
              pregunta.respuesta_Falsa_2,
              pregunta.respuesta_Correcta,
            ];
            respuestasCorrectas.push(pregunta.respuesta_Correcta);
            respuestasOrdenadas.push(
              respuestas.sort(() => Math.random() - 0.5)
            );
          }
        });
      });
      return preguntas;
    } else {
      return console.log(error);
    }
  } catch (error) {
    console.log(error);
  }
};

//Funcion para mostrar las preguntas y las opciones de respuesta
const mostrarPregunta = async (id) => {
  if (!preguntasObtenidas) {
    preguntas = await obtenerPreguntas();
    preguntasObtenidas = true;
  }
  const pregunta = preguntas[id];
  try {
    question_count.innerHTML = `Pregunta ${id + 1} de ${preguntas.length}`;
    if (pregunta.imagen_pregunta != null) {
      imgPregunta.setAttribute("src", pregunta.imagen_pregunta);
    } else {
      imgPregunta.setAttribute(
        "src",
        "/static/icono/iconoAutoescuela-removebg-preview.png"
      );
    }
    question.innerHTML = pregunta.pregunta;
    op1.innerHTML = respuestasOrdenadas[id][0];
    op2.innerHTML = respuestasOrdenadas[id][1];
    op3.innerHTML = respuestasOrdenadas[id][2];
  } catch (error) {
    console.log(error);
  }
};

//Funcion para verificar si se ha marcado algun radioButton y guardando la respuesta, y la posicion de la pregunta
function verificarRadioButtom() {
  if (document.getElementById("flexRadioDefault1").checked) {
    document.getElementById("flexRadioDefault3").checked = false;
    document.getElementById("flexRadioDefault2").checked = false;
    document.getElementById("flexRadioDefault1").checked = true;
    checkMarcado[id] = [true, respuestasOrdenadas[id][0], "0"];
    return true;
  } else if (document.getElementById("flexRadioDefault2").checked) {
    document.getElementById("flexRadioDefault3").checked = false;
    document.getElementById("flexRadioDefault1").checked = false;
    document.getElementById("flexRadioDefault2").checked = true;
    checkMarcado[id] = [true, respuestasOrdenadas[id][1], "1"];
    return true;
  } else if (document.getElementById("flexRadioDefault3").checked) {
    document.getElementById("flexRadioDefault2").checked = false;
    document.getElementById("flexRadioDefault1").checked = false;
    document.getElementById("flexRadioDefault3").checked = true;
    checkMarcado[id] = [true, respuestasOrdenadas[id][2], "2"];
    return true;
  } else {
    document.getElementById("flexRadioDefault2").checked = false;
    document.getElementById("flexRadioDefault1").checked = false;
    document.getElementById("flexRadioDefault3").checked = false;
  }
}

//Funcion para mostrar la respuesta correcta al finalizar el examen y la marca en verde
function seleccionarRespuestaCorrecta(id) {
  if (respuestasCorrectas[id] == respuestasOrdenadas[id][0]) {
    flexRadioDefault1.setAttribute(
      "style",
      "background-color: #fefefe; border: 5px solid #49FF33; border-radius: 50px;"
    );
    flexRadioDefault2.setAttribute("style", "");
    flexRadioDefault3.setAttribute("style", "");
  } else if (respuestasCorrectas[id] == respuestasOrdenadas[id][1]) {
    flexRadioDefault2.setAttribute(
      "style",
      "background-color: #fefefe; border: 5px solid #49FF33; border-radius: 50px;"
    );
    flexRadioDefault1.setAttribute("style", "");
    flexRadioDefault3.setAttribute("style", "");
  } else if (respuestasCorrectas[id] == respuestasOrdenadas[id][2]) {
    flexRadioDefault3.setAttribute(
      "style",
      "background-color: #fefefe; border: 5px solid #49FF33; border-radius: 50px;"
    );
    flexRadioDefault2.setAttribute("style", "");
    flexRadioDefault1.setAttribute("style", "");
  }
}

//Funcion para verificar las respuestas, devolviendo un array de las preguntas falladas y marcar en rojo las respuestas falladas 
//y en verde las correctas de los botones de navegacion inferior
function verificarRespuesta(respuestasUser) {
  let respuestasFalladas = [];
  respuestasCorrectas.forEach((respuesta, index) => {
    let button = document.getElementById(`btn${index + 1}`);

    if (respuesta == respuestasUser[index]) {
      button.setAttribute("style", "background-color: #00D303 !important;");
    } else {
      respuestasFalladas.push(preguntas[index].id_Pregunta);
      button.setAttribute("style", "background-color: #D30000 !important;");
    }
  });
  return respuestasFalladas;
}

//Funciones que se ejecutan al hacer click en los radioButtons
//Cuando seleccionamos una de las 3 opciones esta se guardara en el array checkMarcado
flexRadioDefault1.addEventListener("click", () => {
  let button = document.getElementById(`btn${id + 1}`);
  button.setAttribute("style", "background-color: #0061FF !important;");
  verificarRadioButtom();
});
flexRadioDefault2.addEventListener("click", () => {
  let button = document.getElementById(`btn${id + 1}`);
  button.setAttribute("style", "background-color: #0061FF !important;");
  verificarRadioButtom();
});
flexRadioDefault3.addEventListener("click", () => {
  let button = document.getElementById(`btn${id + 1}`);
  button.setAttribute("style", "background-color: #0061FF !important;");
  verificarRadioButtom();
});

//Funcion que se ejecuta al hacer click en el boton de terminar examen
fin.addEventListener("click", () => {
  examenTerminado = true;
  bloquearRadioButtom();
  verificarRespuesta(respuestasSeleccionadas());
  cambiarVisibilidadBotones();
});

//Funcion que se ejecuta al hacer click en el boton de siguiente pregunta
const next = document.getElementsByClassName("next")[0];
next.addEventListener("click", () => {
  try {
    if (checkMarcado[id][0] == true && id < preguntas.length - 1) {
      ++id;
      mostrarPregunta(id);
      mostrarSeleccion(id);
    } else if (comprobarPreguntasContestadas()) {
      mostrarPregunta(0);
      mostrarSeleccion(0);
      cambiarVisibilidadBotones();
    }
  } catch (error) {
    alert("Seleccione una respuesta");
  }
});

//Funcion que se ejecuta al hacer click en el boton de salir, esta funcion deshabilita los radioButtom para que no se puedan modificar
const bloquearRadioButtom = () => {
  document.getElementById("flexRadioDefault1").disabled = true;
  document.getElementById("flexRadioDefault2").disabled = true;
  document.getElementById("flexRadioDefault3").disabled = true;
};

//Funcion que se ejecuta al hacer click en el boton de salir, esta funcion sustituye el boton de seguiente por el de terminar examen
const cambiarVisibilidadBotones = async () => {
  var end = document.getElementsByClassName("end");
  Array.from(end).forEach((x) => {
    if (x.style.display == "none") {
      x.style.display = "block";
      next.style.display = "none";
    } else {
      x.style.display = "none";
      salir.setAttribute("style", "display: block !important;");
    }
  });
};

//Funcion que se ejecuta al hacer click en el boton de salir, esta funcion comprueba que todas las preguntas hayan sido contestadas
const comprobarPreguntasContestadas = () => {
  let contador = 0;
  checkMarcado.forEach((e) => {
    if (e[0] == true) {
      contador++;
    }
  });
  if (contador == preguntas.length) {
    return true;
  } else {
    return false;
  }
};

//Funcion para obtener el usuario logueado para posteriormente guardar el examen en la base de datos
const obtenerUsuario = async () => {
  try {
    const res = await fetch(URLAPI+"api/usuariologged/");
    const data = await res.json();
    if (data) {
      let usuario = data[0];
      let id_usuario = usuario.dni;
      return id_usuario;
    } else {
      return alert("No hay usuario logeado");
    }
  } catch (error) {
    console.log(error);
  }
};

//Funcion para generar la barra de navegacion de preguntas que se generan segun el numero de preguntas que tenga el examen
const enumPreguntas = async () => {
  try {
    let totalColumnas = preguntas.length / 2;

    for (let i = 1; i <= totalColumnas; i++) {
      row1.innerHTML += `<a class="col " id="colPreguntas"> <button class="btn btn-secondary"  id="btn${i}">${i}</button> </a>`;
    }
    for (let e = totalColumnas + 1; e <= preguntas.length; e++) {
      row2.innerHTML += `<a class="col " id="colPreguntas"> <button class="btn btn-secondary"  id="btn${e}">${e}</button> </a>`;
    }
    for (let a = 0; a < preguntas.length; a++) {
      let btn = document.getElementById(`btn${a + 1}`);
      btn.addEventListener("click", () => {
        id = a;
        mostrarPregunta(id);
        mostrarSeleccion(id);
        if (examenTerminado) {
          seleccionarRespuestaCorrecta(id);
        }
      });
    }
  } catch (error) {
    console.log(error);
  }
};

//Funcion  que en caso de que el usaurio ya haya contestado, muestra la respuesta que ha seleccionado en caso de que vuelva a la pregunta
const mostrarSeleccion = async (id) => {
  try {
    if (checkMarcado[id][2] == "0") {
      document.getElementById("flexRadioDefault1").checked = true;
      document.getElementById("flexRadioDefault2").checked = false;
      document.getElementById("flexRadioDefault3").checked = false;
    } else if (checkMarcado[id][2] == "1") {
      document.getElementById("flexRadioDefault2").checked = true;
      document.getElementById("flexRadioDefault1").checked = false;
      document.getElementById("flexRadioDefault3").checked = false;
    } else if (checkMarcado[id][2] == "2") {
      document.getElementById("flexRadioDefault3").checked = true;
      document.getElementById("flexRadioDefault2").checked = false;
      document.getElementById("flexRadioDefault1").checked = false;
    }
  } catch (error) {
    document.getElementById("flexRadioDefault1").checked = false;
    document.getElementById("flexRadioDefault2").checked = false;
    document.getElementById("flexRadioDefault3").checked = false;
  }
};

//Funcion para obtener todas las respuestas seleccionadas por el usuario
const respuestasSeleccionadas = () => {
  let respuestasUser = [];
  checkMarcado.forEach((check) => {
    respuestasUser.push(check[1]);
  });
  return respuestasUser;
};

//Funcion para guardar el examen realizado por el usaurio en la base de datos
const enviarExamen = async () => {
  try {
    let aprobado = false;
    let usuario = await obtenerUsuario();
    let id_Preguntas_Falladas = verificarRespuesta(respuestasSeleccionadas());
    if (id_Preguntas_Falladas.length <= 3) {
      aprobado = true;
    }
    let examenRealizado = examenSelect.id_Examen;
    const res = await fetch(URLAPI+"api/examen_usuario/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken,
      },
      body: JSON.stringify({
        examen: examenRealizado,
        usuario: usuario,
        preguntas_falladas: id_Preguntas_Falladas,
        aprobado: aprobado,
      }),
    });
    if (res.ok) {
      const jsonResponse = await res.json();
      const { usuario, preguntas_falladas, aprobado, examen } = jsonResponse;
      console.log(
        "Usuario: " +
          usuario +
          " Respuestas falladas: " +
          preguntas_falladas +
          " Aprobado: " +
          aprobado +
          " Examen: " +
          examen
      );
    window.close();
    }
  } catch (error) {
    console.log(error);
  }
};

//Funcion para enviar el examen al pulsar el boton de salir y redirigir al usuario a la pagina de inicio del aulavirtual
salir.addEventListener("click", () => {
  enviarExamen();
});





