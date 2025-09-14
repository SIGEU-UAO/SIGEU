import { dashboardUrl, emailRegex, passwordRegex } from "/static/js/base.js";
import Alert from "/static/js/modules/Alert.js";

let form = document.querySelector("form.form");
let emailInput = document.getElementById("id_email");
let passwordInput = document.getElementById("id_password");

// --- Validaciones ---
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

// --- Fetch ---
 async function handleSubmit(e) {
   e.preventDefault();
 
   if (!validarCampos()) return;
 
   const data = new FormData(form);
   let csrf = (form.querySelector("input[name=csrfmiddlewaretoken]") || {}).value || "";
 
   try {
     let res = await fetch(window.location.href, {
       method: "POST",
        headers: { "X-CSRFToken": csrf, "Accept": "application/json" },
       body: data
     });
     let json = await res.json();
 
     if (res.ok) {
        Alert.success("Has ingresado exitosamente"); setTimeout(() => { window.location.href = dashboardUrl; }, 3000);     } else {
       Alert.error(json.error);
     }
   } catch (err) {
     Alert.error("Error de red. Intenta de nuevo.", err);
     console.error(err);
   }
 }
    