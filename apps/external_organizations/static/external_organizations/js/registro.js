import { telefonoRegex } from "/static/js/base.js";
import Alert from "/static/js/modules/Alert.js";

//* Variables
const validationRules = {
    nit: [
        { check: value => value.length > 0, msg: "El NIT es obligatorio" }
    ],
    nombre: [
        { check: value => value.length > 0, msg: "El nombre es obligatorio" }
    ],
    representante_legal: [
        { check: value => value.length > 0, msg: "El representante legal es obligatorio" }
    ],
    telefono: [
        { check: value => telefonoRegex.test(value), msg: "Teléfono inválido" }
    ],
    ubicacion: [
        { check: value => value.length > 0, msg: "La ubicación es obligatoria" }
    ],
    sector_economico: [
        { check: value => value.length > 0, msg: "El sector económico es obligatorio" }
    ],
    actividad_principal: [
        { check: value => value.length > 0, msg: "La actividad principal es obligatoria" }
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
            setTimeout(() => { window.location.reload(); }, 1500);
        } else {
            Alert.error(json.error || "Error en el registro");
        }
    } catch (err) {
        Alert.error("Error de red. Intenta de nuevo.", err);
        console.error(err);
    }
}