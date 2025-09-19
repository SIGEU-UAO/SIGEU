import { dashboardUrl, emailRegex, passwordRegex } from "/static/js/base.js";
import { handlePasswordVisibility } from "./modules/utils.js";
import { validarFormData, formDataToJSON } from "/static/js/modules/forms/utils.js";
import Alert from "/static/js/modules/Alert.js";

//* Variables
const validationRules = {
    email: [
      { check: value => emailRegex.test(value), msg: "Correo inválido, debe terminar en @uao.edu.co" }
    ],
    password: [
      { check: value => passwordRegex.test(value), msg: "Contraseña inválida" }
    ]
};

//* Selectors
let form = document.querySelector("form.form");
let emailInput = document.getElementById("id_email");
let passwordInput = document.getElementById("id_password");

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

  const csrf = (form.querySelector("input[name=csrfmiddlewaretoken]") || {}).value || "";
  const bodyData = formDataToJSON(formData)

  try {
    let res = await fetch("/users/api/inicio-sesion/", {
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
      Alert.success("Inicio de sesión completado!");
      setTimeout(() => { window.location.href = dashboardUrl; }, 1500);
    } else {
      Alert.error(json.error || "Error en el inicio de sesión");
    }
  } catch (err) {
    Alert.error("Error de red. Intenta de nuevo.", err);
    console.error(err);
  }
}