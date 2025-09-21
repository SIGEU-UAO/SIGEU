import { logoutUrl, loginUrl } from "/static/js/base.js";
import { getCookie } from "/static/js/modules/forms/utils.js";
import Alert from "/static/js/modules/Alert.js";

document.addEventListener("DOMContentLoaded", () => {
    const logoutBtn = document.getElementById("boton-cerrar-sesion");
    logoutBtn.addEventListener("click", logoutConfirmation);
});

async function logoutConfirmation() {
    const result = await Alert.confirmationAlert({
        title: "Cerrar sesión",
        text: "¿Está seguro que desea cerrar sesión?",
        confirmButtonText: "Aceptar",
        cancelButtonText: "Cancelar"
    });

    if (!result.isConfirmed) return;

    try {
        const response = await fetch(logoutUrl, {
            method: "POST",
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            credentials: "same-origin"
        });

        if (response.ok) {
            Alert.success("Cierre de sesión exitoso!");
            setTimeout(() => {
                window.location.href = loginUrl;
            }, 1500);
        } else {
            const data = await response.json();
            Alert.error(data.error || "Error en el cierre de sesión");
        }
    } catch (err) {
        Alert.error("Error de red. Intenta de nuevo.", err);
        console.error(err);
    }
}