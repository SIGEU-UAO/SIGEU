import Alert from "/static/js/modules/Alert.js";
console.log("editar_perfil.js loaded");

document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM loaded, initializing...");
    
    const form = document.querySelector("form.form");
    const editBtn = document.querySelector(".form__edit");
    const cancelBtn = document.getElementById("cancelBtn");
    const formActions = document.querySelector(".form__actions");
    
    console.log("Elements found:", {form, editBtn, cancelBtn, formActions});

    // Campos editables
    const editableFields = [
        document.getElementById("id_nombres"),
        document.getElementById("id_apellidos"),
        document.getElementById("id_telefono"),
        document.getElementById("id_contrasena"),
        document.getElementById("id_contraseña")
    ].filter(field => field !== null);

    // Campo de contraseña (robusto a variaciones de id)
    const passwordFieldEl = document.querySelector('input[name="contraseña"]')
        || document.getElementById("id_contraseña")
        || document.getElementById("id_contrasena");
    
    console.log("Editable fields found:", editableFields);

    // Guardar valores iniciales
    let initialValues = {};
    editableFields.forEach(field => {
        initialValues[field.id] = field.value;
        field.disabled = true;
    });

    // Contenedor para mensajes generales
    let messageContainer = document.createElement("div");
    messageContainer.classList.add("form__message");
    form.prepend(messageContainer);

    function showMessage(text, type = "error") {
        messageContainer.textContent = text;
        messageContainer.style.color = type === "error" ? "red" : "green";
        messageContainer.style.marginBottom = "10px";
    }

    function clearMessage() {
        messageContainer.textContent = "";
    }

    // Crear contenedor de error por campo
    editableFields.forEach(field => {
        let err = document.createElement("div");
        err.classList.add("field-error");
        err.style.color = "red";
        err.style.fontSize = "0.9em";
        err.style.marginTop = "2px";
        field.parentNode.appendChild(err);
    });

    function clearFieldErrors() {
        editableFields.forEach(field => {
            field.parentNode.querySelector(".field-error").textContent = "";
        });
    }

    // Habilitar edición
    editBtn.addEventListener("click", () => {
        console.log("Edit button clicked!");
        
        editableFields.forEach(field => {
            field.disabled = false;
            field.removeAttribute('disabled');
            field.readOnly = false;
            field.removeAttribute('readonly');
        });
        
        console.log("Fields enabled");
        
        if (editableFields.length > 0) {
            editableFields[0].focus();
        }
        
        // Limpiar mensajes
        clearMessage();
        clearFieldErrors();
        
        // Mostrar botones de acción
        if (formActions) {
            formActions.classList.remove("hide");
            console.log("Buttons shown");
        } else {
            console.error("formActions not found!");
        }
    });

    // Cancelar cambios
    cancelBtn.addEventListener("click", () => {
        console.log("Cancel button clicked!");
        
        editableFields.forEach(field => {
            field.value = initialValues[field.id];
            field.disabled = true;
            field.setAttribute('disabled', 'true');
        });
        
        clearMessage();
        clearFieldErrors();
        
        // Ocultar botones de acción
        if (formActions) {
            formActions.classList.add("hide");
            console.log("Buttons hidden");
        }
    });

    // Guardar cambios
    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        clearMessage();
        clearFieldErrors();

        let valid = true;
        editableFields.forEach(field => {
            const isPasswordField = passwordFieldEl && field === passwordFieldEl;
            // Permitir que la contraseña esté vacía
            if (isPasswordField) return;
            if (!field.value.trim()) {
                const errNode = field.parentNode.querySelector(".field-error");
                if (errNode) {
                    errNode.textContent = `El campo "${field.name}" no puede estar vacío.`;
                }
                valid = false;
            }
        });
        if (!valid) return;

        // Confirmación si se está cambiando la contraseña
        if (passwordFieldEl && passwordFieldEl.value.trim().length > 0) {
            const result = await Alert.confirmationAlert({
                title: "Cambiar contraseña",
                text: "¿Está seguro que desea cambiar la contraseña?",
                confirmButtonText: "Aceptar",
                cancelButtonText: "Cancelar",
            });
            const confirmed = (result && typeof result === 'object') ? !!result.isConfirmed : !!result;
            if (!confirmed) {
                // Volver a la vista por defecto (cancelado)
                editableFields.forEach(field => {
                    field.disabled = true;
                    field.setAttribute('disabled', 'true');
                });
                if (formActions) {
                    formActions.classList.add("hide");
                }
                return; // cancelar envío
            }
        }

        console.log("Preparing to submit form...");
        
        // Crear FormData con todos los campos (incluidos los deshabilitados)
        const formData = new FormData();
        
        // Agregar CSRF token
        const csrf = form.querySelector("input[name=csrfmiddlewaretoken]");
        if (csrf) {
            formData.append('csrfmiddlewaretoken', csrf.value);
        }
        
        // Agregar todos los campos del formulario
        const allInputs = form.querySelectorAll('input, select, textarea');
        allInputs.forEach(input => {
            if (input.name && input.name !== 'csrfmiddlewaretoken') {
                formData.append(input.name, input.value || '');
            }
        });
        
        console.log("FormData prepared");

        try {
            const res = await fetch("/perfil/", {
                method: "POST",
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                },
                body: formData
            });

            if (!res.ok) {
                // Leer JSON de error
                let errorJson = await res.json().catch(() => null);
                if (errorJson && errorJson.errors) {
                    // Mostrar errores por campo
                    for (let key in errorJson.errors) {
                        let field = document.getElementById(`id_${key}`);
                        if (field) {
                            const errNode = field.parentNode.querySelector(".field-error");
                            if (errNode) {
                                errNode.textContent = errorJson.errors[key].join(", ");
                            }
                        }
                    }
                    // No continuar con el flujo de éxito si hubo errores de validación
                    return;
                }
                // Si viene un error general en formato { error: "mensaje" }, mostrarlo arriba del formulario
                if (errorJson && errorJson.error) {
                    showMessage(errorJson.error, "error");
                    return;
                }
                // Si no hay JSON o estructura conocida, mostrar mensaje genérico pero no como error de red
                showMessage("No se pudo procesar la solicitud. Revisa los datos e inténtalo de nuevo.", "error");
                return;
            }

            const data = await res.json();
            console.log("Success response:", data);
            Alert.success("Perfil actualizado correctamente!");

            // Limpiar el campo de contraseña después de éxito, si existe
            if (passwordFieldEl) {
                passwordFieldEl.value = "";
            }

            // Actualizar valores iniciales y deshabilitar campos
            editableFields.forEach(field => {
                initialValues[field.id] = field.value;
                field.disabled = true;
                field.setAttribute('disabled', 'true');
            });
            
            // Ocultar botones de acción
            const formActions = document.querySelector(".form__actions");
            if (formActions) {
                formActions.classList.add("hide");
            }

        } catch (err) {
             Alert.error("Error de red. Intenta de nuevo.", err);
            console.error(err);
        }
    });
});
