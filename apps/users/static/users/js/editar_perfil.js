// Import Alert class for Notyf notifications
import Alert from "/static/js/modules/classes/Alert.js";
import API from "/static/js/modules/classes/API.js";

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

// Clear password error when user types
passwordFieldEl.addEventListener('input', () => {
    // Mantener listener por compatibilidad; sin acciones ya que los errores se muestran por alertas
});

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
    if (!pwdVal) {
        formData.delete('contraseña');
    }
    // Use API.post method which handles CSRF automatically
    const result = await API.post("/users/api/editar-perfil/", formData);
    
    if (result.error) {
        // Mostrar mensajes de error mediante alertas (ej. teléfono duplicado)
        let msg = '¡Error actualizando el perfil!';
        if (result.data && result.data.error) {
            const err = result.data.error;
            if (typeof err === 'string') {
                msg = err;
            } else if (err.telefono && err.telefono.length) {
                msg = err.telefono[0] || 'El teléfono ya está registrado.';
            }
        }
        Alert.error(msg);
        return;
    }
    
    // Success case
    Alert.success("Perfil actualizado correctamente!");
    
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
