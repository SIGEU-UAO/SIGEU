import { loginUrl, numeroIdentificacionRegex, emailRegex, passwordRegex, telefonoRegex } from "/static/js/base.js";
import Alert from "/static/js/modules/Alert.js";

const form = document.querySelector("form.form");
const rolSelect = document.getElementById("id_rol");
const camposEstudiante = document.getElementById("campos-estudiante");
const camposDocente = document.getElementById("campos-docente");
const camposSecretaria = document.getElementById("campos-secretaria");

const documentoInput = document.getElementById("id_documento");
const nombreInput = document.getElementById("id_nombre");
const apellidoInput = document.getElementById("id_apellido");
const emailInput = document.getElementById("id_email");
const telefonoInput = document.getElementById("id_telefono");
const password1Input = document.getElementById("id_password1");
const password2Input = document.getElementById("id_password2");

//Campos oppcionales segun el rol
const codigoEstudianteInput = document.getElementById("id_codigo_estudiante");
const programaSelect = document.getElementById("id_programa");
const unidadAcademicaSelect = document.getElementById("id_unidadAcademica");
const facultadSelect = document.getElementById("id_facultad");

//Icons
const passwordInfoBtn = document.querySelector(".form__group:has(#id_password1) .icon__btn:last-of-type");
const passwordEyeBtns = document.querySelectorAll(".form__group:has(.password-field) .icon__btn:first-of-type")

//Events Listeners
document.addEventListener("DOMContentLoaded", () => {
  passwordInfoBtn.addEventListener("click", Alert.showPasswordInfo)
  passwordEyeBtns.forEach(btn => btn.addEventListener("click", handlePasswordVisibility));
  rolSelect.addEventListener("change", handleFormVisibility);
  form.addEventListener("submit", handleSubmit);
})

function handlePasswordVisibility(e) {
    const passwordInput = e.target.closest(".form__group").querySelector("input");
    
    //Change visibility
    const isPassword = passwordInput.type === "password";
    passwordInput.type = isPassword ? "text" : "password";

    const icon = e.target;
        icon.src = isPassword 
            ? "/static/authentication/assets/icons/eye-slash.svg"
            : "/static/authentication/assets/icons/eye.svg";
}

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
  let rol = rolSelect.value;
  if (documentoInput.value.trim() === "" || !numeroIdentificacionRegex.test(documentoInput.value.trim())) { Alert.error("Documento de identidad invalido"); return false; }
  if (nombreInput.value.trim() === "") { Alert.error("Ingresa el nombre"); return false; }
  if (apellidoInput.value.trim() === "") { Alert.error("Ingresa el apellido"); return false; }
  if (emailInput.value.trim() === "" || !emailRegex.test(emailInput.value.trim())) { Alert.error("Correo invalido"); return false; }
  if (telefonoInput.value.trim() === "" || !telefonoRegex.test(telefonoInput.value.trim())) { Alert.error("Telefono invalido"); return false; }
  if (password1Input.value.trim() === "" || !passwordRegex.test(password1Input.value.trim())) { Alert.error("Contraseña invalida"); return false; }
  if (password2Input.value.trim() === "" || !passwordRegex.test(password2Input.value.trim())) { Alert.error("Contraseña invalida"); return false; }
  if (password1Input.value !== password2Input.value) { Alert.error("Las contraseñas no coinciden"); return false; }

  if (rol === "estudiante") {
    if (codigoEstudianteInput.value.trim() === "") { Alert.error("Ingresa el código de estudiante"); return false; }
    if (!programaSelect.value) { Alert.error("Selecciona un programa"); return false; }
  } else if (rol === "docente") {
    if (!unidadAcademicaSelect.value) { Alert.error("Selecciona una unidad académica"); return false; }
  } else if (rol === "secretaria") {
    if (!facultadSelect.value) { Alert.error("Selecciona una facultad"); return false; }
  }
  return true;
}

async function handleSubmit(e) {
  e.preventDefault();
  if (!validarCampos()) return;

  let csrf = (form.querySelector("input[name=csrfmiddlewaretoken]") || {}).value || "";

  const bodyData = JSON.stringify({
    documento: documentoInput.value.trim(),
    nombre: nombreInput.value.trim(),
    apellido: apellidoInput.value.trim(),
    email: emailInput.value.trim(),
    telefono: telefonoInput.value.trim(),
    password1: password1Input.value.trim(),
    password2: password2Input.value.trim(),
    rol: rolSelect.value,
    codigo_estudiante: codigoEstudianteInput?.value.trim(),
    programa: programaSelect?.value,
    unidadAcademica: unidadAcademicaSelect?.value,
    facultad: facultadSelect?.value
  });

  try {
    let res = await fetch("/registro/api/", {
      method: "POST",
      headers: {
        "X-CSRFToken": csrf,
        "Content-Type": "application/json",
        "Accept": "application/json"
      },
      body: bodyData
    });

    let json = await res.json();

    if (res.ok) {
      Alert.success(`${rolSelect.value.charAt(0).toUpperCase() + rolSelect.value.slice(1).toLowerCase()} registrado exitosamente`);
      setTimeout(() => { window.location.href = loginUrl; }, 1500);
    } else {
      Alert.error(json.error || "Error en el registro");
    }
  } catch (err) {
    Alert.error("Error de red. Intenta de nuevo.", err);
    console.error(err);
  }
}
