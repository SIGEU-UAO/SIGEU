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
const password1Field = document.getElementById("id_new_password1");
const password2Field = document.getElementById("id_new_password2");

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

