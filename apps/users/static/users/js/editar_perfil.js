// Imports
import { emailRegex, passwordRegex } from "/static/js/base.js";
import { validarFormData, formDataToJSON } from "/static/js/modules/forms/utils.js";
import Alert from "/static/js/modules/Alert.js";

//* Reglas de validación
const validationRules = {
  email: [
    { check: value => emailRegex.test(value), msg: "Correo inválido, debe terminar en @uao.edu.co" }
  ],
  contraseña: [
    { check: value => !value || passwordRegex.test(value), msg: "Contraseña inválida" }
  ],
};

document.addEventListener("DOMContentLoaded", () => {
  //* Selectores
  const form = document.querySelector("form.form");
  const editButton = document.querySelector(".form__edit");
  const formActions = document.querySelector(".form__actions");
  const cancelButton = document.getElementById("cancelBtn");
  const formFields = document.querySelectorAll(".form input, .form textarea, .form select");

  //* Estado inicial
  const originalValues = {};
  formFields.forEach(field => {
    originalValues[field.name] = field.value;
  });

  //* Funciones
  function handleEdit(e) {
    e.preventDefault();
    if (formActions) formActions.classList.remove("hide");
    formFields.forEach(field => {
      field.removeAttribute("readonly");
      field.removeAttribute("disabled");
    });
    if (editButton) editButton.style.display = "none";
  }

  function handleCancel(e) {
    e.preventDefault();
    if (formActions) formActions.classList.add("hide");
    formFields.forEach(field => {
      if (originalValues.hasOwnProperty(field.name)) {
        field.value = originalValues[field.name];
      }
      field.setAttribute("readonly", "true");
      if (field.dataset.wasDisabled === "true") {
        field.setAttribute("disabled", "true");
      }
    });
    if (editButton) editButton.style.display = "inline-block";
  }

  async function handleSubmit(e) {
    e.preventDefault();
    if (!form) return;

    // Validar
    const formData = new FormData(form);
    if (!validarFormData(formData, validationRules)) return;

    const csrf = (form.querySelector("input[name=csrfmiddlewaretoken]") || {}).value || "";
    const bodyData = formDataToJSON(formData);

    try {
      const res = await fetch("/users/api/editar/", {
        method: "POST",
        headers: {
          "X-CSRFToken": csrf,
          "Content-Type": "application/json",
          "Accept": "application/json",
          "X-Requested-With": "XMLHttpRequest"
        },
        body: bodyData   // bodyData is already a JSON string from formDataToJSON
      });

      const json = await res.json();

      if (res.ok && json.message) {
        Alert.success(json.message || "Perfil actualizado correctamente");

        // Actualizar valores originales
        ["nombres", "apellidos", "telefono", "codigo_estudiante"].forEach(field => {
          if (json[field] !== undefined) {
            const f = form.querySelector(`[name="${field}"]`);
            if (f) {
              f.value = json[field];
              originalValues[field] = json[field];
            }
          }
        });

        formFields.forEach(field => field.setAttribute("readonly", "true"));
        if (formActions) formActions.classList.add("hide");
        if (editButton) editButton.style.display = "inline-block";
      } else if (json.errors) {
        let html = "";
        for (const [field, errs] of Object.entries(json.errors)) {
          html += `<p><strong>${field}:</strong> ${errs.join(", ")}</p>`;
        }
        Alert.error(html);
      } else {
        Alert.error(json.error || "No se pudieron guardar los cambios. Intenta nuevamente.");
      }
    } catch (err) {
      Alert.error("Error de red. Intenta de nuevo.", err);
      console.error(err);
    }
  }

  //* Listeners
  if (editButton) editButton.addEventListener("click", handleEdit);
  if (cancelButton) cancelButton.addEventListener("click", handleCancel);
  if (form) form.addEventListener("submit", handleSubmit);

  
});
