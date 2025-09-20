document.addEventListener("DOMContentLoaded", () => {
    const logoutBtn = document.getElementById("boton-cerrar-sesion");
    if (!logoutBtn) return;

    const logoutUrl = logoutBtn.dataset.logoutUrl;
    const loginUrl = logoutBtn.dataset.loginUrl;

    logoutBtn.addEventListener("click", async () => {
        const result = await Swal.fire({
            title: "Cerrar sesión",
            text: "¿Está seguro que desea cerrar sesión?",
            //icon: "warning",
            showCancelButton: true,
            confirmButtonText: "Aceptar",
            cancelButtonText: "Cancelar",
            confirmButtonColor: "#ff7aa2",
            cancelButtonColor: "#666666",
            reverseButtons: true
        });

        if (!result.isConfirmed) return;

        try {
            const response = await fetch(logoutUrl, {
                method: "POST",
                headers: { "X-CSRFToken": getCookie("csrftoken") },
                credentials: "same-origin"
            });

            if (response.ok) {
                await Swal.fire({
                    title: "Sesión cerrada",
                    text: "Has salido del sistema correctamente",
                    icon: "success",
                    timer: 1500,
                    showConfirmButton: false
                });
                window.location.href = loginUrl;
            } else {
                const data = await response.json();
                Swal.fire("Error", data.error || "No se pudo cerrar sesión", "error");
            }
        } catch (err) {
            console.error("Error en logout:", err);
            Swal.fire("Error", "Hubo un problema al cerrar sesión", "error");
        }
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
