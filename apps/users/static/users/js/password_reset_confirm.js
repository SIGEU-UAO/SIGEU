import { passwordRegex } from "/static/js/base.js";
import { handlePasswordVisibility } from "./modules/utils.js";
import { validarFormData } from "/static/js/modules/forms/utils.js";
import Alert from "/static/js/modules/classes/Alert.js";

//* Variables
const validationRules = {
    new_password1: [
        { check: value => passwordRegex.test(value), msg: "Contraseña inválida" }
    ],
    new_password2: [
        { check: value => passwordRegex.test(value), msg: "Contraseña inválida" },
        { check: (value, formData) => value === formData.get("new_password1"), msg: "Las contraseñas no coinciden" }
    ]
};

//* Selectors
const form = document.querySelector("form.form");
const passwordEyeBtns = document.querySelectorAll(".form__group:has(.password-field) .icon__btn:first-of-type, .form__group:has(input[type='password']) .icon__btn:first-of-type");
const passwordInfoBtn = document.querySelector(".form__group:has(#id_new_password1) .icon__btn:last-of-type");

//* Event Listeners
document.addEventListener("DOMContentLoaded", () => {
    // Mostrar mensajes de Django usando Notyf (migrado desde password_reset.js)
    showDjangoMessages();

    // Configurar campos de contraseña
    setupPasswordFields();
    
    // Event listeners para botones de ojo (mostrar/ocultar contraseña)
    passwordEyeBtns.forEach(btn => {
        btn.addEventListener("click", handlePasswordVisibility);
    });
    
    // Event listener para botón de información
    if (passwordInfoBtn) {
        passwordInfoBtn.addEventListener("click", Alert.showPasswordInfo);
    }
    
    // Event listener para el formulario
    if (form) {
        form.addEventListener("submit", handleSubmit);
    }
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

function setupPasswordFields() {
    // Agregar clase password-field a los campos de contraseña para compatibilidad
    const password1Field = document.getElementById("id_new_password1");
    const password2Field = document.getElementById("id_new_password2");
    
    if (password1Field) {
        password1Field.classList.add("password-field");
        password1Field.setAttribute("type", "password");
    }
    
    if (password2Field) {
        password2Field.classList.add("password-field");
        password2Field.setAttribute("type", "password");
    }
}

function handleSubmit(e) {
    e.preventDefault();
    
    // Validar formulario usando las reglas definidas
    const formData = new FormData(form);
    if (!validarFormData(formData, validationRules)) {
        return;
    }
    
    // Si la validación pasa, enviar el formulario
    Alert.success("Se ha enviado un correo de recuperación");
    form.submit();
}

// Función para mostrar validación en tiempo real (opcional)
function setupRealTimeValidation() {
    const password1Field = document.getElementById("id_new_password1");
    const password2Field = document.getElementById("id_new_password2");
    
    if (password1Field) {
        password1Field.addEventListener("input", (e) => {
            validatePasswordStrength(e.target.value);
        });
    }
    
    if (password2Field) {
        password2Field.addEventListener("input", (e) => {
            validatePasswordMatch(password1Field.value, e.target.value);
        });
    }
}

function validatePasswordStrength(password) {
    const isValid = passwordRegex.test(password);
    const field = document.getElementById("id_new_password1");
    const parent = field.closest(".form__group");
    
    // Remover clases anteriores
    parent.classList.remove("form__group--valid", "form__group--invalid");
    
    if (password.length > 0) {
        if (isValid) {
            parent.classList.add("form__group--valid");
        } else {
            parent.classList.add("form__group--invalid");
        }
    }
}

function validatePasswordMatch(password1, password2) {
    const field = document.getElementById("id_new_password2");
    const parent = field.closest(".form__group");
    
    // Remover clases anteriores
    parent.classList.remove("form__group--valid", "form__group--invalid");
    
    if (password2.length > 0) {
        if (password1 === password2 && passwordRegex.test(password2)) {
            parent.classList.add("form__group--valid");
        } else {
            parent.classList.add("form__group--invalid");
        }
    }
}

// Inicializar validación en tiempo real si se desea
// setupRealTimeValidation();
