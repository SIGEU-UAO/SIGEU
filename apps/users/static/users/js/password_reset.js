import Alert from "/static/js/modules/classes/Alert.js";

//* Variables
// Regex to validate institutional email @uao.edu.co
const emailRegex = /^[a-zA-Z0-9._%+-]+@uao\.edu\.co$/;

// Manual validation in handleSubmit

//* Selectors
const form = document.querySelector("form.form--reset");
const emailField = document.getElementById("id_email");

//* Event Listeners
document.addEventListener("DOMContentLoaded", () => {
    // Mostrar mensajes de Django usando Notyf
    showDjangoMessages();
    
    // Configure form validation
    if (form) {
        form.addEventListener("submit", handleSubmit);
    }
    
    // Configure real-time validation
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
    
    // Only validate basic format in frontend. Existence validation will be done by the backend.
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
    
    // If basic validation passes, send to server
    form.submit();
}

function setupRealTimeValidation() {
    if (emailField) {
        emailField.addEventListener("input", (e) => {
            // Clear server errors when the user starts typing
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
    
    // Remove previous classes
    parent.classList.remove("form__group--valid", "form__group--invalid");
    
    // Only remove real-time validation errors (not server errors)
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
    
    // Create and display error message (marked as JS error)
    const errorDiv = document.createElement('div');
    errorDiv.className = 'form__error js-error';
    errorDiv.innerHTML = `<p>${message}</p>`;
    parent.appendChild(errorDiv);
}
