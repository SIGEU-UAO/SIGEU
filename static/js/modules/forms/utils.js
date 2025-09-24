import Alert from "../classes/Alert.js"

//* Valida campos de un FormData (Reutilizable para todos los forms)
export function validarFormData(formData, rules = {}) {
  for (let [campo, valor] of formData.entries()) {
    let val = valor.trim();

    // Default validation: empty
    if (!val) {
      Alert.error(`El campo ${campo} es obligatorio`);
      return false;
    }

    // Additional validations defined in rules
    if (rules[campo]) {
      for (let { check, msg } of rules[campo]) {
        if (!check(val, formData)) {  // formData is passed in case you need to validate against another field
          Alert.error(msg);
          return false;
        }
      }
    }
  }
  return true;
}

//* Retorna un JSON a partir de un formData
export function formDataToJSON(formData) {
  let obj = {};
  formData.forEach((val, key) => obj[key] = val.trim());
  return JSON.stringify(obj);
}

export function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

export function cleanContainer(container){
  while (container.firstElementChild) {
    container.firstElementChild.remove();
  }
}