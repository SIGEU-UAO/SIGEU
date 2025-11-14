import { dashboardUrl, emailRegex, passwordRegex } from "/static/js/base.js";
import { handlePasswordVisibility } from "./modules/utils.js";
import { validarFormData } from "/static/js/modules/forms/utils.js";
import Alert from "/static/js/modules/classes/Alert.js";
import API from "/static/js/modules/classes/API.js";

//* Variables
const validationRules = {
    email: [
      { check: value => emailRegex.test(value), msg: "Correo inválido, debe terminar en @uao.edu.co" }
    ],
    password: [
      { check: value => passwordRegex.test(value), msg: "Contraseña incorrecta" }
    ]
};

//* Selectors
let form = document.querySelector("form.form");

//Icons
const passwordEyeBtns = document.querySelector(".form__group:has(.password-field) .icon__btn:first-of-type")

document.addEventListener("DOMContentLoaded", () => {
  passwordEyeBtns.addEventListener("click", handlePasswordVisibility);
  form.addEventListener("submit", handleSubmit);
})

async function handleSubmit(e) {
  e.preventDefault();

  //Validate form
  let formData = new FormData(form);
  if (!validarFormData(formData, validationRules)) return;

  //Fetch the endpoint
  const result = await API.post("/users/api/inicio-sesion/", formData);
  if (result.error) return;

  Alert.success("Inicio de sesión completado!");
  setTimeout(() => { window.location.href = dashboardUrl; }, 1500);
}