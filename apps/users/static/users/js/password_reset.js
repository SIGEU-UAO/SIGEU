import Alert from "/static/js/modules/classes/Alert.js";

//* Variables
// Regex para validar email institucional @uao.edu.co
const emailRegex = /^[a-zA-Z0-9._%+-]+@uao\.edu\.co$/;

// Validación manual en handleSubmit

//* Selectors
const form = document.querySelector("form.form--reset");
const emailField = document.getElementById("id_email");

//* Event Listeners
document.addEventListener("DOMContentLoaded", () => {
    // Mostrar mensajes de Django usando Notyf
    showDjangoMessages();
    
    // Configurar validación del formulario
    if (form) {
        form.addEventListener("submit", handleSubmit);
    }
    
    // Configurar validación en tiempo real
    setupRealTimeValidation();
});

//* Functions
function showDjangoMessages() {
    const alertElements = document.querySelectorAll('.alert');
    
    alertElements.forEach(alertElement => {
        const message = alertElement.textContent.trim();
        
        if (alertElement.classList.contains('alert--error')) {
            Alert.error(message);
        } else if (alertElement.classList.contains('alert--success')) {
            Alert.success(message);
        } else if (alertElement.classList.contains('alert--info')) {
            Alert.info(message);
        }
        alertElement.style.display = 'none';
    });
}

function handleSubmit(e) {
    e.preventDefault();
    
    // Solo validar formato básico en frontend
    // La validación de existencia la hará el backend
    const formData = new FormData(form);
    const email = formData.get('email');
    
    if (!email || !email.trim()) {
        Alert.error('El correo electrónico es requerido');
        return;
    }
    
    if (!emailRegex.test(email.trim())) {
        Alert.error('Correo inválido');
        return;
    }
    
    // Si la validación básica pasa, enviar al servidor
    form.submit();
}

function setupRealTimeValidation() {
    if (emailField) {
        emailField.addEventListener("input", (e) => {
            // Limpiar errores del servidor cuando el usuario empiece a escribir
            const parent = emailField.closest(".form__group");
            if (parent) {
                const serverError = parent.querySelector(".form__error:not(.js-error)");
                if (serverError) {
                    serverError.remove();
                }
            }
            validateEmailField(e.target.value);
        });
        
        emailField.addEventListener("blur", (e) => {
            validateEmailField(e.target.value);
        });
    }
}

function validateEmailField(email) {
    if (!emailField) return;
    
    const parent = emailField.closest(".form__group");
    if (!parent) return;
    
    // Remover clases anteriores
    parent.classList.remove("form__group--valid", "form__group--invalid");
    
    // Solo remover errores de validación en tiempo real (no los del servidor)
    const existingError = parent.querySelector(".form__error.js-error");
    if (existingError) {
        existingError.remove();
    }
    
    if (email && email.trim().length > 0) {
        if (emailRegex.test(email.trim())) {
            parent.classList.add("form__group--valid");
        } else {
            parent.classList.add("form__group--invalid");
            showFieldError(emailField, "Correo inválido");
        }
    }
}

function showFieldError(field, message) {
    const parent = field.closest(".form__group");
    if (!parent) return;
    
    // Crear y mostrar mensaje de error (marcado como error JS)
    const errorDiv = document.createElement('div');
    errorDiv.className = 'form__error js-error';
    errorDiv.innerHTML = `<p>${message}</p>`;
    parent.appendChild(errorDiv);
}
