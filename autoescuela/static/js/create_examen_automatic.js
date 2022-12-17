var btnGenerar = document.getElementById("btnGenerar");
var PreguntasPermiso = [];
//Variables para guardar los datos del examen
var miform = document.getElementById("form"); //Variable para obtener datos del formulario
var csrftoken = miform.querySelector("[name=csrfmiddlewaretoken]").value; //Variable para guardar el token csrf

btnGenerar.addEventListener("click", async function () {
    //Funcion para generar el examen
    try {
        const res = await fetch("http://127.0.0.1:8000/api/pregunta/");
        const data = await res.json();

        if (data) {
            var preguntas = data;
            var i = 0;
            var permiso = seleccionarPermiso();
            let maxPregtuas = maxPreguntas(permiso);

            while (i < maxPregtuas) {
                var random = Math.floor(Math.random() * preguntas.length);
                if (
                    preguntas[random].permiso == permiso &&
                    !PreguntasPermiso.includes(preguntas[random])
                ) {
                    PreguntasPermiso.push(preguntas[random]);
                    i++;
                }
            }
            mostrarPreguntas(PreguntasPermiso);
        }
    } catch (err) {
        console.error(err);
    }
});

function seleccionarPermiso() {
    //Funcion para seleccionar el permiso
    let permisos = document.getElementById("permisos").value;
    let permiso;
    switch (permisos) {
        case "1":
            permiso = "A";
            break;
        case "2":
            permiso = "B";
            break;
        case "3":
            permiso = "C";
            break;
        case "4":
            permiso = "D";
            break;
    }
    return permiso;
}

function maxPreguntas(permiso) {
    //Funcion para seleccionar el permiso
    let cantidad;
    switch (permiso) {
        case "A":
            cantidad = 30;
            break;
        case "B":
            cantidad = 30;
            break;
        case "C":
            cantidad = 20;
            break;
        case "D":
            cantidad = 20;
            break;
    }
    return cantidad;
}

function mostrarPreguntas(preguntas) {
    //Funcion para mostrar las preguntas
    let html = "";
    preguntas.forEach((pregunta) => {
        html += `
            <tr>
                <td scope="col">${pregunta.pregunta}</td>
            </tr>
            `;
    });
    document.getElementById("preguntasSeleccionadas").innerHTML = html;
    
}

document
    .getElementById("btnRegistrar")
    .addEventListener("click", async function () {
        console.log("token", csrftoken);
        try {
            var id_preguntas = [];
            PreguntasPermiso.forEach((pregunta) => {
                id_preguntas.push(pregunta.id_Pregunta);
            });
            let nombre = document.getElementById("nombre_Examen").value;
            console.log(id_preguntas);
            const res = await fetch("http://127.0.0.1:8000/api/examen/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftoken,
                },
                body: JSON.stringify({
                    nombre_Examen: nombre,
                    preguntas: id_preguntas,
                }),
            });
            if (res.ok) {
                const jsonResponse = await res.json();
                const { nombre_Examen, preguntas } = jsonResponse;
                alert("Examen" + nombre_Examen + " reado correctamente");
            }
        } catch (err) {
            console.error(err);
        }
    });
