import { loginUrl, numeroIdentificacionRegex, emailRegex, passwordRegex,telefonoRegex } from "/static/js/base.js";
import Alert from "/static/js/modules/Alert.js";


// --- base (form y botón) ---
let form = document.querySelector("form.form");
let submitBtn = document.querySelector(".form__button");

let rolSelect = document.getElementById("id_rol");
let camposEstudiante = document.getElementById("campos-estudiante");
let camposDocente = document.getElementById("campos-docente");
let camposSecretaria = document.getElementById("campos-secretaria");

// --- inputs base ---
let documentoInput = document.getElementById("id_documento");
let nombreInput = document.getElementById("id_nombre");
let apellidoInput = document.getElementById("id_apellido");
let emailInput = document.getElementById("id_email");
let telefonoInput = document.getElementById("id_telefono");
let password1Input = document.getElementById("id_password1");
let password2Input = document.getElementById("id_password2");

// --- inputs por rol ---
let codigoEstudianteInput = document.getElementById("id_codigo_estudiante");
let programaSelect = document.getElementById("id_programa");
let unidadAcademicaSelect = document.getElementById("id_unidadAcademica");
let facultadSelect = document.getElementById("id_facultad");

// --- eventos ---
rolSelect.addEventListener("change", handleFormVisibility);
form.addEventListener("submit", handleSubmit);

function handleFormVisibility(e) {
  const rol = e.target.value;
  camposEstudiante.classList.add("hide");
  camposDocente.classList.add("hide");
  camposSecretaria.classList.add("hide");

  if (rol === "estudiante") camposEstudiante.classList.remove("hide");
  if (rol === "docente") camposDocente.classList.remove("hide");
  if (rol === "secretaria") camposSecretaria.classList.remove("hide");
}

function validarCampos() {
  let rol = rolSelect.value

  // base requeridos
  if (documentoInput.value.trim() === "" || !numeroIdentificacionRegex.test(documentoInput.value.trim())) { Alert.error("Documento de identidad invalido"); return false; }
  if (nombreInput.value.trim() === "" ) { Alert.error("Ingresa el nombre"); return false; }
  if (apellidoInput.value.trim() === "" )  { Alert.error("Ingresa el apellido"); return false; }
  if (emailInput.value.trim() === "" || !emailRegex.test(emailInput.value.trim())){ Alert.error("Correo invalido"); return false; }
  if (telefonoInput.value.trim() === "" || !telefonoRegex.test(telefonoInput.value.trim())) { Alert.error("Telefono invalido"); return false; }
  if (password1Input.value.trim() === "" || !passwordRegex.test(password1Input.value.trim())){ Alert.error("Contraseña invalida"); return false; }
  if (password2Input.value.trim() === "" || !passwordRegex.test(password2Input.value.trim())){ Alert.error("Contraseña invalida"); return false; }
  if (password1Input.value !== password2Input.value) { Alert.error("Las contraseñas no coinciden"); return false; }

  // por rol
  if (rol === "estudiante") {
    if (codigoEstudianteInput.value.trim() === "" ) { Alert.error("Ingresa el código de estudiante"); return false; }
    if (!programaSelect.value)               { Alert.error("Selecciona un programa"); return false; }
  } else if (rol === "docente") {
    if (!unidadAcademicaSelect.value)        { Alert.error("Selecciona una unidad académica"); return false; }
  } else if (rol === "secretaria") {
    if (!facultadSelect.value)               { Alert.error("Selecciona una facultad"); return false; }
  }

  return true;
}

async function handleSubmit(e) {
  e.preventDefault();

  if (!validarCampos()) return;

  const data = new FormData(form);
  let csrf = (form.querySelector("input[name=csrfmiddlewaretoken]") || {}).value || "";

  try {
    let res = await fetch(window.location.href, {
      method: "POST",
      headers: { "X-CSRFToken": csrf },
      body: data
    });
    let json = await res.json();

    if (res.ok) {
      Alert.success(`${rolSelect.value.charAt(0).toUpperCase() + rolSelect.value.slice(1).toLowerCase()} registrado exitosamente`);
      setTimeout(() => { window.location.href = loginUrl; }, 3000);
    } else {
      Alert.error(json.error);
    }
  } catch (err) {
    Alert.error("Error de red. Intenta de nuevo.", err);
    console.error(err);
  }
}

