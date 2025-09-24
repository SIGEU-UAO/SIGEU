import { loginUrl, numeroIdentificacionRegex, emailRegex, passwordRegex, telefonoRegex } from "/static/js/base.js";
import { handlePasswordVisibility } from "./modules/utils.js";
import { validarFormData } from "/static/js/modules/forms/utils.js";
import Alert from "/static/js/modules/classes/Alert.js";
import API from "/static/js/modules/classes/API.js";

//* Variables
const validationRules = {
    documento: [
      { check: value => numeroIdentificacionRegex.test(value), msg: "Documento inválido" }
    ],
    email: [
      { check: value => emailRegex.test(value), msg: "Correo inválido, debe terminar en @uao.edu.co" }
    ],
    telefono: [
      { check: value => telefonoRegex.test(value), msg: "Teléfono inválido" }
    ],
    password1: [
      { check: value => passwordRegex.test(value), msg: "Contraseña inválida" }
    ],
    password2: [
      { check: value => passwordRegex.test(value), msg: "Contraseña inválida" },
      { check: (value, formData) => value === formData.get("password1"), msg: "Las contraseñas no coinciden" }
    ],
    codigo_estudiante: [
      { check: (value, formData) => formData.get("rol") !== "estudiante" || value !== "", msg: "Ingresa el código de estudiante" }
    ]
};

//* Selectors
const form = document.querySelector("form.form");
const rolSelect = document.getElementById("id_rol");
const camposEstudiante = document.getElementById("campos-estudiante");
const camposDocente = document.getElementById("campos-docente");
const camposSecretaria = document.getElementById("campos-secretaria");

//Icons
const passwordInfoBtn = document.querySelector(".form__group:has(#id_password1) .icon__btn:last-of-type");
const passwordEyeBtns = document.querySelectorAll(".form__group:has(.password-field) .icon__btn:first-of-type")

//*Events Listeners
document.addEventListener("DOMContentLoaded", () => {
  passwordInfoBtn.addEventListener("click", Alert.showPasswordInfo)
  passwordEyeBtns.forEach(btn => btn.addEventListener("click", handlePasswordVisibility));
  rolSelect.addEventListener("change", handleFormVisibility);
  form.addEventListener("submit", handleSubmit);
})

//* Functions
function handleFormVisibility(e) {
  const rol = e.target.value;

  const bloques = {
    estudiante: camposEstudiante,
    docente: camposDocente,
    secretaria: camposSecretaria
  };

  Object.values(bloques).forEach(block => {
    block.classList.add("hide");
    block.querySelectorAll("input, select, textarea").forEach(el => {
      el.disabled = true;
    });
  });

  if (bloques[rol]) {
    bloques[rol].classList.remove("hide");
    bloques[rol].querySelectorAll("input, select, textarea").forEach(el => {
      el.disabled = false;
    });
  }
}

async function handleSubmit(e) {
  e.preventDefault();

  // Validate form
  let formData = new FormData(form);
  if (!validarFormData(formData, validationRules)) return;

  //Fetch the endpoint
  const result = await API.post("/users/api/registro/", formData);
  if (result.error) return;

  Alert.success(`${rolSelect.value.charAt(0).toUpperCase() + rolSelect.value.slice(1).toLowerCase()} registrado exitosamente`);
  setTimeout(() => { window.location.href = loginUrl; }, 1500);
}