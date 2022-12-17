
let menuPermisos = document.getElementById("menuPermisos");
let menuLista = document.getElementById("menuLista");

menuPermisos.addEventListener("mouseover", () => {
    menuLista.style.display = "block";
});

menuLista.addEventListener("mouseout", () => {
    menuLista.style.display = "none";
});
