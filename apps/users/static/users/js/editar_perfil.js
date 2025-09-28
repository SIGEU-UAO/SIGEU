const form = document.querySelector("form.form");
const editBtn = document.querySelector(".form__edit");
const cancelBtn = document.getElementById("cancelBtn");
const formActions = document.querySelector(".form__actions");

// Editable fields
const editableFields = [
    document.getElementById("id_nombres"),
    document.getElementById("id_apellidos"),
    document.getElementById("id_telefono"),
    document.getElementById("id_contraseña")
];

// Password field
const passwordFieldEl = document.querySelector('input[name="contraseña"]');

// Save initial values and disable fields
let initialValues = {};
editableFields.forEach(field => {
    initialValues[field.id] = field.value;
    field.disabled = true;
});

// Import Alert class for Notyf notifications
import Alert from "/static/js/modules/classes/Alert.js";

function clearFieldErrors() {
    document.querySelectorAll('.field-error').forEach(node => {
        node.textContent = '';
    });
}

// Initialize containers and messages
function initPerfilForm() {
    if (!form) return;
    
    // Create error containers per field if they don't exist
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

// Execute initialization
initPerfilForm();

// Enable editing
function handleEdit(e) {
    e.preventDefault();

    // Clear old errors when starting edit
    clearFieldErrors();
    
    editableFields.forEach(field => {
        if (field) {
            field.disabled = false;
            field.removeAttribute('disabled');
            field.readOnly = false;
            field.removeAttribute('readonly');
        }
    });
    
    if (editableFields.length > 0 && editableFields[0]) {
        editableFields[0].focus();
    }
    
    if (formActions) {
        formActions.classList.remove("hide");
    }
}

// Cancel changes
function handleCancel(e) {
    e.preventDefault();
    
    editableFields.forEach(field => {
        if (field) {
            field.value = initialValues[field.id];
            field.disabled = true;
            field.setAttribute('disabled', 'true');
        }
    });
    
    if (formActions) {
        formActions.classList.add("hide");
    }
    // Clear errors on cancel
    clearFieldErrors();
}

// Save changes
async function handleSubmit(e) {
    e.preventDefault();
    
    // Password confirmation if changed
    if (passwordFieldEl && passwordFieldEl.value.trim().length > 0) {
        const confirmed = confirm("¿Está seguro que desea cambiar la contraseña?");
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
    
    // Build formData 
    const formData = new FormData(form);
    
    // If password is empty, remove it from formData to avoid overwriting with empty
    const pwdVal = (formData.get('contraseña') || '').trim();
    if (!pwdVal) {
        formData.delete('contraseña');
    }
    
    // Prepare headers and body json
    const csrf = (form.querySelector("input[name=csrfmiddlewaretoken]") || {}).value || "";
    
    const bodyData = {};
    for (let [key, value] of formData.entries()) {
        bodyData[key] = value;
    }

    // Ensure disabled-but-required fields are present
    const readVal = (name) => {
        const el = form.querySelector(`input[name="${name}"]`);
        return el ? el.value : "";
    };
    if (!bodyData.numeroIdentificacion) bodyData.numeroIdentificacion = readVal("numeroIdentificacion");
    if (!bodyData.nombres) bodyData.nombres = readVal("nombres");
    if (!bodyData.apellidos) bodyData.apellidos = readVal("apellidos");
    if (!bodyData.email) bodyData.email = readVal("email");
    // Note: If the codigo_estudiante field doesn't exist in the DOM, we don't send it.
    if (document.querySelector('input[name="codigo_estudiante"]')) {
        if (!bodyData.codigo_estudiante) bodyData.codigo_estudiante = readVal("codigo_estudiante");
    }
    
    try {
        // Use the correct URL: /perfil/ instead of /users/api/perfil/
        const res = await fetch("/perfil/", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrf,
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            body: JSON.stringify(bodyData)
        });
        
        if (!res.ok) {
            let errorJson = await res.json().catch(() => null);
            
            if (errorJson && errorJson.error) {
                const err = errorJson.error;
                // If error is a dict of field errors, paint them
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
                // If it's a string, show error notification
                Alert.error(String(err));
                return;
            }
            // If there's no JSON or known structure, show a generic message
            Alert.error("No se pudo procesar la solicitud. Revisa los datos e inténtalo de nuevo.");
            return;
        }
        
        const data = await res.json();
        // Clear previous errors before showing success
        clearFieldErrors();
        Alert.success("Perfil actualizado correctamente!");
        
        // Clean the password field
        if (passwordFieldEl) {
            passwordFieldEl.value = "";
        }
        
        // Update initial values and disable fields
        editableFields.forEach(field => {
            initialValues[field.id] = field.value;
            field.disabled = true;
            field.setAttribute('disabled', 'true');
        });
        
        // Hide action buttons
        if (formActions) {
            formActions.classList.add("hide");
        }
        
    } catch (err) {
        Alert.error("Error de red. Intenta de nuevo.");
    }
}

// Add event listeners
editBtn.addEventListener("click", handleEdit);

if (cancelBtn) {
    cancelBtn.addEventListener("click", handleCancel);
}

// Clear password error when user types
if (passwordFieldEl) {
    passwordFieldEl.addEventListener('input', () => {
        const errNode = passwordFieldEl.parentNode.querySelector('.field-error');
        if (errNode) errNode.textContent = '';
    });
}

form.addEventListener("submit", handleSubmit);
