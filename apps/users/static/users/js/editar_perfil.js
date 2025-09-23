import Alert from "/static/js/modules/Alert.js";
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
    // Container for form messages
    let messageContainer = document.createElement("div");
    messageContainer.classList.add("form__message");
    form.prepend(messageContainer);

    function showMessage(text, type = "error") {
        messageContainer.textContent = text;
        messageContainer.style.color = type === "error" ? "red" : "green";
        messageContainer.style.marginBottom = "10px";
    }

   

    // create error message containers for each field
    editableFields.forEach(field => {
        let err = document.createElement("div");
        err.classList.add("field-error");
        err.style.color = "red";
        err.style.fontSize = "0.9em";
        err.style.marginTop = "2px";
        field.parentNode.appendChild(err);
    });

    

    // enable editing
    editBtn.addEventListener("click", () => {
        editableFields.forEach(field => {
            field.disabled = false;
            field.removeAttribute('disabled');
            field.readOnly = false;
            field.removeAttribute('readonly');
        });
        if (editableFields.length > 0) {
            editableFields[0].focus();
        }
        
        // clear previous messages
        
        
        // show action buttons
        
            formActions.classList.remove("hide");
       
    
    });

    // cancel changes
    cancelBtn.addEventListener("click", () => {
        editableFields.forEach(field => {
            field.value = initialValues[field.id];
            field.disabled = true;
            field.setAttribute('disabled', 'true');
        });
        
        
        
        // hide action buttons
      
            formActions.classList.add("hide");
        
    });

    // save changes
    async function handleSubmit(e) {
        e.preventDefault();

        let valid = true;
        editableFields.forEach(field => {
            const isPasswordField = passwordFieldEl && field === passwordFieldEl;
            // allow empty password field (means no change)
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

        // confirm if password is being changed
        if (passwordFieldEl && passwordFieldEl.value.trim().length > 0) {
            const result = await Alert.confirmationAlert({
                title: "Cambiar contraseña",
                text: "¿Está seguro que desea cambiar la contraseña?",
                confirmButtonText: "Aceptar",
                cancelButtonText: "Cancelar",
            });
            const confirmed = (result && typeof result === 'object') ? !!result.isConfirmed : !!result;
            if (!confirmed) {
                // go back to  initial state
                editableFields.forEach(field => {
                    field.disabled = true;
                    field.setAttribute('disabled', 'true');
                });
                if (formActions) {
                    formActions.classList.add("hide");
                }
                return; // cancel sending
            }
        }
        //  create FormData with all fields (including disabled ones)
        const formData = new FormData();
        
        // add CSRF token if present
        const csrf = form.querySelector("input[name=csrfmiddlewaretoken]");
        if (csrf) {
            formData.append('csrfmiddlewaretoken', csrf.value);
        }
        
        // add all form inputs to formData
        const allInputs = form.querySelectorAll('input, select, textarea');
        allInputs.forEach(input => {
            if (input.name && input.name !== 'csrfmiddlewaretoken') {
                formData.append(input.name, input.value || '');
            }
        });
        try {
            const res = await fetch("/perfil/", {
                method: "POST",
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                },
                body: formData
            });

            if (!res.ok) {
                let errorJson = await res.json().catch(() => null);
                if (errorJson && errorJson.errors) {
                    // show field-specific errors
                    for (let key in errorJson.errors) {
                        let field = document.getElementById(`id_${key}`);
                        if (field) {
                            const errNode = field.parentNode.querySelector(".field-error");
                            if (errNode) {
                                errNode.textContent = errorJson.errors[key].join(", ");
                            }
                        }
                    }
                    
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
