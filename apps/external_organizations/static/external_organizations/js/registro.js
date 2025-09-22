import { telefonoRegex, nitRegex } from "/static/js/base.js";
import { validarFormData, formDataToJSON } from "/static/js/modules/forms/utils.js";

import Alert from "/static/js/modules/Alert.js";

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
document.addEventListener("DOMContentLoaded", () => {
    form.addEventListener("submit", handleSubmit);
});

//* Functions
async function handleSubmit(e) {
    e.preventDefault();

    // Validar formulario
    let formData = new FormData(form);
    if (!validarFormData(formData, validationRules)) return;

    const csrf = (form.querySelector("input[name=csrfmiddlewaretoken]") || {}).value || "";
    const bodyData = formDataToJSON(formData);

    try {
        let res = await fetch("/orgs/api/registro/", {
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
            Alert.success("Organización registrada exitosamente");
            form.reset();
        } else {
            Alert.error(json.error || "Error en el registro");
        }
    } catch (err) {
        Alert.error("Error de red. Intenta de nuevo.", err);
        console.error(err);
    }
}
