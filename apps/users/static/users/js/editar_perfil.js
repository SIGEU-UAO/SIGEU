import Alert from "/static/js/modules/Alert.js";
import { telefonoRegex, passwordRegex } from "/static/js/base.js";
import { validarFormData, formDataToJSON } from "/static/js/modules/forms/utils.js";
    const form = document.querySelector("form.form");
    const editBtn = document.querySelector(".form__edit");
    const cancelBtn = document.getElementById("cancelBtn");
    const formActions = document.querySelector(".form__actions");
    // editable fields
    const editableFields = [
        document.getElementById("id_nombres"),
        document.getElementById("id_apellidos"),
        document.getElementById("id_telefono"),
       
        document.getElementById("id_contraseña")
    ].filter(field => field !== null);

    // Campo de contraseña (robusto a variaciones de id)
    const passwordFieldEl = document.querySelector('input[name="contraseña"]')
        || document.getElementById("id_contraseña")
        || document.getElementById("id_contrasena");
   
        
    // Save initial values and disable fields
    let initialValues = {};
    editableFields.forEach(field => {
        initialValues[field.id] = field.value;
        field.disabled = true;
    });
    // Container for form messages (initialized in initPerfilForm)
    let messageContainer;

    function showMessage(text, type = "error") {
        if (!messageContainer) return;
        messageContainer.textContent = text;
        messageContainer.style.color = type === "error" ? "red" : "green";
        messageContainer.style.marginBottom = "10px";
    }

   

    // Inicialización de contenedores y mensajes
    function initPerfilForm() {
        if (!form) return;
        // Crear contenedor de mensajes si no existe
        if (!messageContainer) {
            messageContainer = document.createElement("div");
            messageContainer.classList.add("form__message");
            form.prepend(messageContainer);
        }
        // Crear contenedores de error por campo si no existen
        editableFields.forEach(field => {
            if (!field) return;
            let err = field.parentNode.querySelector('.field-error');
            if (!err) {
                err = document.createElement('div');
                err.classList.add('field-error');
                err.style.color = 'red';
                err.style.fontSize = '0.9em';
                err.style.marginTop = '2px';
                field.parentNode.appendChild(err);
            }
        });
    }

    // Ejecutar inicialización al cargar el módulo
    initPerfilForm();

    

    // enable editing
    function handleEdit(e) {
        e.preventDefault();
        editableFields.forEach(field => {
            field.disabled = false;
            field.removeAttribute('disabled');
            field.readOnly = false;
            field.removeAttribute('readonly');
        });
        if (editableFields.length > 0) {
            editableFields[0].focus();
        }
        if (formActions) {
            formActions.classList.remove("hide");
        }
    }
    editBtn.addEventListener("click", handleEdit);

    // cancel changes
    function handleCancel(e) {
        e.preventDefault();
        editableFields.forEach(field => {
            field.value = initialValues[field.id];
            field.disabled = true;
            field.setAttribute('disabled', 'true');
        });
        if (formActions) {
            formActions.classList.add("hide");
        }
    }
    cancelBtn.addEventListener("click", handleCancel);

    // save changes
    async function handleSubmit(e) {
        e.preventDefault();

        // password confirmation if changed
        if (passwordFieldEl && passwordFieldEl.value.trim().length > 0) {
            const result = await Alert.confirmationAlert({
                title: "Cambiar contraseña",
                text: "¿Está seguro que desea cambiar la contraseña?",
                confirmButtonText: "Aceptar",
                cancelButtonText: "Cancelar",
            });
            const confirmed = (result && typeof result === 'object') ? !!result.isConfirmed : !!result;
            if (!confirmed) {
                editableFields.forEach(field => {
                    field.disabled = true;
                    field.setAttribute('disabled', 'true');
                });
                if (formActions) {
                    formActions.classList.add("hide");
                }
                return;
            }
        }

        //buildear formData 
        const formData = new FormData(form);

        // if password is empty, remove it from formData to avoid overwriting with empty
        const pwdVal = (formData.get('contraseña') || '').trim();
        if (!pwdVal) {
            formData.delete('contraseña');
        }

        // rules for validation
        const rules = {
            telefono: [
                { check: value => telefonoRegex.test(value), msg: "Teléfono inválido" }
            ]
        };
        if (pwdVal) {
            rules['contraseña'] = [
                { check: value => passwordRegex.test(value), msg: "Contraseña inválida" }
            ];
        }

        // generic form validation
        if (!validarFormData(formData, rules)) return;

        // prepare headers and body json
        const csrf = (form.querySelector("input[name=csrfmiddlewaretoken]") || {}).value || "";
        const bodyData = formDataToJSON(formData);

        try {
            const res = await fetch("/users/api/perfil/", {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrf,
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                body: bodyData
            });

            if (!res.ok) {
                let errorJson = await res.json().catch(() => null);
                if (errorJson && errorJson.error) {
                    const err = errorJson.error;
                    // if error is a dict of field errors, paint them
                    if (typeof err === 'object' && err !== null) {
                        for (let key in err) {
                            let field = document.getElementById(`id_${key}`);
                            if (field) {
                                const errNode = field.parentNode.querySelector(".field-error");
                                if (errNode) {
                                    const msgs = Array.isArray(err[key]) ? err[key] : [String(err[key])];
                                    errNode.textContent = msgs.join(", ");
                                }
                            }
                        }
                        return;
                    }
                    // If it's a string, show it above the form
                    showMessage(String(err), "error");
                    return;
                }
                // If there's no JSON or known structure, show a generic message but not as a network error
                showMessage("No se pudo procesar la solicitud. Revisa los datos e inténtalo de nuevo.", "error");
                return;
            }

            const data = await res.json();
            Alert.success("Perfil actualizado correctamente!");

            // clean the password field
            if (passwordFieldEl) {
                passwordFieldEl.value = "";
            }

            // Update initial values and disable fields
            editableFields.forEach(field => {
                initialValues[field.id] = field.value;
                field.disabled = true;
                field.setAttribute('disabled', 'true');
            });
            
            // hide action buttons
            const formActions = document.querySelector(".form__actions");
            if (formActions) {
                formActions.classList.add("hide");
            }

        } catch (err) {
             Alert.error("Error de red. Intenta de nuevo.", err);
            
        }
    }

    form.addEventListener("submit", handleSubmit);
