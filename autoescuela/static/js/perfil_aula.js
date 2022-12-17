const URLAPI = "http://127.0.0.1:8000/"; // Cambiar por la URL de la API


const cargaInicial = async () => {//carga inicial
  await cargarExamenesUsuario();
};

window.addEventListener("load", async () => {//carga inicial
  await cargaInicial();
});

const cargarExamenesUsuario = async () => {
  //carga los examenes del usuario
  try {
    const response = await fetch(URLAPI + "api/cargarExamenesUsuario/");
    const examenes = await response.json();
    //console.log(examenes[0].get_usuario_class);
    calcularMediaExamenes(examenes);
    obtenerDatos(examenes);
    //mostrarExamenes(examenes);
    return examenes;
  } catch (error) {
    console.log(error);
  }
};

const calcularMediaExamenes = (examenes) => {
  //calcula la media de los examenes
  let media = 0;
  for (let i = 0; i < examenes.length; i++) {
    if (examenes[i].aprobado == true) {
      media += 1;
    }
  }
  media = (media / examenes.length) * 100;
  media = media.toFixed(2);
  valorBarra(media);
};

const valorBarra = (media) => {
  //cambia el valor de la barra de progreso
  barProgreso.setAttribute(`style`, `width: ${media}%`);
  barProgreso.setAttribute(`aria-valuenow`, `${media}`);
  barProgreso.innerHTML = `${media}%`;
  if (media < 50) {
    barProgreso.classList.remove("bg-success");
    barProgreso.classList.add("bg-danger");
  } else {
    barProgreso.classList.remove("bg-danger");
    barProgreso.classList.add("bg-success");
  }
};

const obtenerDatos = async (examenesUsuario) => {
  //obtiene los datos de los examenes
  try {
    const resPreguntas = await fetch(URLAPI + "api/pregunta/");
    const preguntas = await resPreguntas.json();
    const resExamenes = await fetch(URLAPI + "api/examen/");
    const examenes = await resExamenes.json();

    let arrayExamenesUsuario = [];
    let arrayPreguntas = [];
    let totalPreguntasFalladas = [];
    examenes.forEach((examen) => {
      examenesUsuario.forEach((examenUsuario) => {
        if (examen.id_Examen == examenUsuario.examen) {
          arrayExamenesUsuario.push(examen);
          examen.preguntas.forEach((pregunta) => {
            arrayPreguntas.push(pregunta);
            examenUsuario.preguntas_falladas.forEach((preguntaFallada) => {
              if (pregunta == preguntaFallada) {
                totalPreguntasFalladas.push(pregunta);
              }
            });
          });
        }
      });
    });

    let arrayClasePreguntasFalladas = [];
    let arrayClasePreguntas = [];
    preguntas.forEach((pregunta) => {
      arrayPreguntas.forEach((preguntasExamenes) => {
        if (pregunta.id_Pregunta == preguntasExamenes) {
          arrayClasePreguntas.push(pregunta);
        }
      });
      totalPreguntasFalladas.forEach((preguntaFallada) => {
        if (pregunta.id_Pregunta == preguntaFallada) {
          arrayClasePreguntasFalladas.push(pregunta);
        }
      });
    });
    await calcularMediaTemas(arrayClasePreguntas, arrayClasePreguntasFalladas);
  } catch (error) {
    console.log(error);
  }
};
var index;
const calcularMediaTemas = async (
  //calcula la media de los temas
  arrayClasePreguntas,
  arrayClasePreguntasFalladas
) => {
  let media = 0;
  let porcentajeFallosTema = [];
  const resTemas = await fetch(URLAPI + "api/tema/");
  const temas = await resTemas.json();

  let arrayTemasFallados = ordenarPorTemas(temas, arrayClasePreguntasFalladas);
  let arrayTemas = ordenarPorTemas(temas, arrayClasePreguntas);
  
  
  for (let i = 0; i < temas.length; i++) {
    let porcentaje;
   
    porcentaje = (arrayTemasFallados[i] / arrayTemas[i]) * 100;
    porcentaje = porcentaje.toFixed(2);
    porcentajeFallosTema[i]=porcentaje;
    if (
      porcentajeFallosTema[i] == null ||
      porcentajeFallosTema[i] == undefined
    ) {
      porcentajeFallosTema[i]=0;
    } else if (isNaN(porcentajeFallosTema[i])) {
      porcentajeFallosTema[i]=0;
    } 
    
    console.log(porcentajeFallosTema[i]);
  }

  mostrarPorcentajeTema(porcentajeFallosTema, temas);
  return porcentajeFallosTema;
};

function ordenarPorTemas(temas, preguntas) {
  //ordena las preguntas por temas
  let totalPreTem = 0;
  let arrayTemas = [];
  temas.forEach((tema) => {
    preguntas.forEach((preguntas) => {
      if (tema.id_Tema == preguntas.tema) {
        totalPreTem++;
      }
    });
    arrayTemas.push(totalPreTem);
    totalPreTem = 0;
  });
  return arrayTemas;
}

const mostrarPorcentajeTema = (porcentajeFallosTema, temas) => {
  //muestra el porcentaje de fallos por tema
  try {
    let botonTemas = document.getElementsByClassName("dropmenuTema")[0];

    //console.log(botonTemas);
    temas.forEach((tema, i) => {
      const element = temas[i];
      botonTemas.innerHTML += `<li><a class="dropdown-item tema${i}" href="#" style=" z-index:999 ">Tema = ${tema.tema}</a></li>`;
      //console.log(porcentaje);
    });

    //console.log(porcentajeFallosTema.length);
    let porcentajeHTML = document.getElementsByClassName("colPorcentaje")[0];
    temas.forEach((tema, i) => {
      let porcentaje = porcentajeFallosTema[i];
      //console.log(porcentaje);
      let button = document.getElementsByClassName(`tema${i}`)[0];
      button.addEventListener("click", () => {
        porcentajeHTML.innerHTML = `
                <div style="margin-top: 10px">
                        <h5>Tema ${tema.tema}</h5>
                </div>
                <div class="progress">
                    <div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" aria-label="Animated striped example" aria-valuenow="75" aria-valuemin="0" id="barProgreso${i}" aria-valuemax="100" style="width:${porcentaje}%">${porcentaje}%</div>
                </div>`;
        if (porcentaje > 50) {
          document
            .getElementById(`barProgreso${i}`)
            .classList.remove("bg-danger");
          document
            .getElementById(`barProgreso${i}`)
            .classList.add("bg-success");
        } else {
          document
            .getElementById(`barProgreso${i}`)
            .classList.remove("bg-success");
          document.getElementById(`barProgreso${i}`).classList.add("bg-danger");
        }
      });
    });
  } catch (error) {
    console.log(error);
  }
};
