// Import Alert class for Notyf notifications
import Alert from "/static/js/modules/classes/Alert.js";
import API from "/static/js/modules/classes/API.js";
import { logoutUrl, loginUrl } from "/static/js/base.js";
import { getCookie } from "/static/js/modules/forms/utils.js";

//* Variables
let initialValues = {};

//* Selectors
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

//* Events Listeners
editBtn.addEventListener("click", handleEdit);
cancelBtn.addEventListener("click", handleCancel);
form.addEventListener("submit", handleSubmit);

// Initialize form
editableFields.forEach(field => {
    initialValues[field.id] = field.value;
    field.disabled = true;
});

//* Functions
// Enable editing
function handleEdit(e) {
    e.preventDefault();
    
    editableFields.forEach(field => {
        field.disabled = false;
        field.removeAttribute('disabled');
        field.readOnly = false;
        field.removeAttribute('readonly');
    });
    
   
    editableFields[0].focus();
    
    
    formActions.classList.remove("hide");
}

// Cancel changes
function handleCancel(e) {
    e.preventDefault();
    
    editableFields.forEach(field => {
        field.value = initialValues[field.id];
        field.disabled = true;
        field.setAttribute('disabled', 'true');
    });
    
    formActions.classList.add("hide");
}

// Save changes
async function handleSubmit(e) {
    e.preventDefault();
    
    // Password confirmation if changed
    if (passwordFieldEl && passwordFieldEl.value.trim().length > 0) {
        const result = await Alert.confirmationAlert({
            title: "Cambiar contraseña",
            text: "¿Está seguro que desea cambiar la contraseña?",
            confirmButtonText: "Aceptar",
            cancelButtonText: "Cancelar"
        });
        
        if (!result.isConfirmed) {
            
            editableFields.forEach(field => {
                field.disabled = true;
                field.setAttribute('disabled', 'true');
            });
            formActions.classList.add("hide");
            return;
        }
    }
    
    // Build formData 
    const formData = new FormData(form);
    
    // If password is empty, remove it from formData to avoid overwriting with empty
    const pwdVal = (formData.get('contraseña') || '').trim();
    const changedPassword = !!pwdVal;
    if (!pwdVal) {
        formData.delete('contraseña');
    }
    // Use API.post method which handles CSRF automatically
    const result = await API.post("/users/api/editar-perfil/", formData);

    
    if (result.error) {
        
        return;
    }
    
    // Success case
    Alert.success("Perfil actualizado correctamente!");

    // If password was changed, log the user out and redirect to login
    if (changedPassword) {
        try {
            const response = await fetch(logoutUrl, {
                method: "POST",
                headers: { "X-CSRFToken": getCookie("csrftoken") },
                credentials: "same-origin"
            });

            if (response.ok) {
                Alert.success("La contraseña fue actualizada. Se cerrará la sesión...");
                setTimeout(() => {
                    window.location.href = loginUrl;
                }, 1500);
                return; // avoid continuing UI updates as we will redirect
            } else {
                // If logout API failed, notify the user but keep them logged in
                let data;
                try { data = await response.json(); } catch {}
                Alert.error((data && data.error) || "No se pudo cerrar sesión automáticamente. Por favor, cierra sesión manualmente.");
            }
        } catch (err) {
            Alert.error("Error de red al cerrar sesión. Intenta de nuevo o cierra sesión manualmente.");
            console.error(err);
        }
    }
    
    // Clean the password field
    passwordFieldEl.value = "";
    
    // Update initial values and disable fields
    editableFields.forEach(field => {
        initialValues[field.id] = field.value;
        field.disabled = true;
        field.setAttribute('disabled', 'true');
    });
    
    // Hide action buttons
    formActions.classList.add("hide");
}
