// Función principal que se ejecuta cuando el DOM está listo
document.addEventListener('DOMContentLoaded', function() {
    console.log('Iniciando editar perfil...');
    
    const form = document.querySelector("form.form");
    const editBtn = document.querySelector(".form__edit");
    const cancelBtn = document.getElementById("cancelBtn");
    const formActions = document.querySelector(".form__actions");
    
    // Verificar que los elementos críticos existan
    if (!editBtn) {
        console.error('Botón de editar no encontrado');
        return;
    }
    if (!form) {
        console.error('Formulario no encontrado');
        return;
    }
    if (!formActions) {
        console.error('Botones de acción no encontrados');
        return;
    }
    
    console.log('Elementos encontrados correctamente');
    
    // editable fields
    const editableFields = [
        document.getElementById("id_nombres"),
        document.getElementById("id_apellidos"),
        document.getElementById("id_telefono"),
        document.getElementById("id_contraseña")
    ].filter(field => field !== null);
    
    console.log('Campos editables encontrados:', editableFields.length);
    
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
    
    // Container for form messages
    let messageContainer;
    
    function showMessage(text, type = "error") {
        if (!messageContainer) {
            messageContainer = document.createElement("div");
            messageContainer.classList.add("form__message");
            messageContainer.style.marginBottom = "10px";
            messageContainer.style.padding = "10px";
            messageContainer.style.borderRadius = "8px";
            form.prepend(messageContainer);
        }
        messageContainer.textContent = text;
        messageContainer.style.color = type === "error" ? "red" : "green";
        messageContainer.style.backgroundColor = type === "error" ? "#ffe6e6" : "#e6ffe6";
    }
    
    // Inicialización de contenedores y mensajes
    function initPerfilForm() {
        if (!form) return;
        
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
    
    // Ejecutar inicialización
    initPerfilForm();
    
    // enable editing
    function handleEdit(e) {
        e.preventDefault();
        console.log('Botón de editar clickeado');
        
        editableFields.forEach(field => {
            if (field) {
                field.disabled = false;
                field.removeAttribute('disabled');
                field.readOnly = false;
                field.removeAttribute('readonly');
                console.log('Campo habilitado:', field.id);
            }
        });
        
        if (editableFields.length > 0 && editableFields[0]) {
            editableFields[0].focus();
        }
        
        if (formActions) {
            formActions.classList.remove("hide");
            console.log('Botones de acción mostrados');
        }
    }
    
    // cancel changes
    function handleCancel(e) {
        e.preventDefault();
        console.log('Botón de cancelar clickeado');
        
        editableFields.forEach(field => {
            if (field) {
                field.value = initialValues[field.id];
                field.disabled = true;
                field.setAttribute('disabled', 'true');
            }
        });
        
        if (formActions) {
            formActions.classList.add("hide");
            console.log('Botones de acción ocultados');
        }
    }
    
    // save changes
    async function handleSubmit(e) {
        e.preventDefault();
        console.log('Formulario enviado');
        
        // password confirmation if changed
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
        
        // build formData 
        const formData = new FormData(form);
        
        // if password is empty, remove it from formData to avoid overwriting with empty
        const pwdVal = (formData.get('contraseña') || '').trim();
        if (!pwdVal) {
            formData.delete('contraseña');
        }
        
        // prepare headers and body json
        const csrf = (form.querySelector("input[name=csrfmiddlewaretoken]") || {}).value || "";
        const bodyData = {};
        for (let [key, value] of formData.entries()) {
            bodyData[key] = value;
        }
        
        try {
            // Usar la URL correcta: /perfil/ en lugar de /users/api/perfil/
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
                // If there's no JSON or known structure, show a generic message
                showMessage("No se pudo procesar la solicitud. Revisa los datos e inténtalo de nuevo.", "error");
                return;
            }
            
            const data = await res.json();
            showMessage("Perfil actualizado correctamente!", "success");
            
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
            if (formActions) {
                formActions.classList.add("hide");
            }
            
        } catch (err) {
            console.error('Error:', err);
            showMessage("Error de red. Intenta de nuevo.", "error");
        }
    }
    
    // Agregar event listeners
    editBtn.addEventListener("click", handleEdit);
    console.log('Event listener agregado al botón de editar');
    
    if (cancelBtn) {
        cancelBtn.addEventListener("click", handleCancel);
        console.log('Event listener agregado al botón de cancelar');
    }
    
    form.addEventListener("submit", handleSubmit);
    console.log('Event listener agregado al formulario');
    
    console.log('Editar perfil inicializado correctamente');
});