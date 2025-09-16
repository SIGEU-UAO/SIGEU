import { dashboardUrl, emailRegex, passwordRegex } from "/static/js/base.js";
import Alert from "/static/js/modules/Alert.js";

let form = document.querySelector("form.form");
let emailInput = document.getElementById("id_email");
let passwordInput = document.getElementById("id_password");

function validarCampos() {
  if (emailInput.value.trim() === "" || !emailRegex.test(emailInput.value.trim())) {
    Alert.error("Correo inválido");
    return false;
  }
  if (passwordInput.value.trim() === "" || !passwordRegex.test(passwordInput.value.trim())) {
    Alert.error("Contraseña inválida");
    return false;
  }
  return true;
}

async function handleSubmit(e) {
  e.preventDefault();

  if (!validarCampos()) return;

  let csrf = (form.querySelector("input[name=csrfmiddlewaretoken]") || {}).value || "";

  const bodyData = JSON.stringify({
    email: emailInput.value.trim(),
    password: passwordInput.value.trim()
  });

  try {
    let res = await fetch("/inicio-sesion/api/", {
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
      Alert.success("Has ingresado exitosamente");
      setTimeout(() => { window.location.href = dashboardUrl; }, 2000);
    } else {
      Alert.error(json.error || "Error en el inicio de sesión");
    }
  } catch (err) {
    Alert.error("Error de red. Intenta de nuevo.", err);
    console.error(err);
  }
}

form.addEventListener("submit", handleSubmit);