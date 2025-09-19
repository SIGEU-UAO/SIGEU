import Alert from "../Alert.js"

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