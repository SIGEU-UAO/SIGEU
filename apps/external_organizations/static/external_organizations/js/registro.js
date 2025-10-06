import { telefonoRegex, nitRegex } from "/static/js/base.js";
import { validarFormData } from "/static/js/modules/forms/utils.js";

import Alert from "/static/js/modules/classes/Alert.js";
import API from "/static/js/modules/classes/API.js";

//* Variables
const validationRules = {
    nit: [
        { check: value => nitRegex.test(value), msg: "El NIT no cumple el formato válido (ej. 12345678-9)" }
        
    ],
    telefono: [
        { check: value => telefonoRegex.test(value), msg: "Teléfono inválido" }
    ]
};

//* Selectors
const form = document.querySelector("form.form");

//* Events Listeners
form.addEventListener("submit", handleSubmit);

//* Functions
async function handleSubmit(e) {
    e.preventDefault();

    // Validate form
    let formData = new FormData(form);
    if (!validarFormData(formData, validationRules)) return;

    //Fetch the endpoint
    const result = await API.post("/orgs/api/registro/", formData);
    if (result.error) return;

    Alert.success("Organización registrada exitosamente");
    setTimeout(() => { window.location.href = "/orgs/listado/"; }, 1500);
}