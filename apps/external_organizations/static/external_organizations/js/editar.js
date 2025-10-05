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

    // Validar formulario
    const formData = new FormData(form);
    if (!validarFormData(formData, validationRules)) return;

    // Obtener el ID desde la URL actual (ej. /orgs/listado/orgs/editar/7/)
    const parts = window.location.pathname.split("/").filter(Boolean);
    const pk = parts[parts.length - 1]; // Toma el último número

    const apiUrl = `/orgs/api/${pk}/update/`;

    // Enviar al endpoint correcto
    const result = await API.put(apiUrl, formData);
    if (result.error) return;

    Alert.success("Organización actualizada exitosamente");
    setTimeout(() => { window.location.href = "/orgs/listado/"; }, 1500);
}