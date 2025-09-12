const rolSelect = document.getElementById("id_rol")
const camposEstudiante = document.getElementById("campos-estudiante") 
const camposDocente = document.getElementById("campos-docente") 
const camposSecretaria = document.getElementById("campos-secretaria") 

rolSelect.addEventListener("change", handleFormVisibility) 

function handleFormVisibility(e) { 

const rol = e.target.value; 

// Ocultar todos los campos 
// 
camposEstudiante.classList.add("hide"); 
camposDocente.classList.add("hide"); 
camposSecretaria.classList.add("hide"); 

// Mostrar solo el contenedor correspondiente 
if (rol === "estudiante") camposEstudiante.classList.remove("hide"); 
if (rol === "docente") camposDocente.classList.remove("hide"); 
if (rol === "secretaria") camposSecretaria.classList.remove("hide"); }
