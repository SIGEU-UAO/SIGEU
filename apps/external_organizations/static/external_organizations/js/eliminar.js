import { getCookie } from "/static/js/modules/forms/utils.js";
import Alert from "/static/js/modules/classes/Alert.js";

document.addEventListener("DOMContentLoaded", () => {
    document.addEventListener("click", async (event) => {
        const btn = event.target.closest("button[data-id]");
        if (!btn) return;

        const id = btn.dataset.id;
        const url = `/orgs/api/delete/${id}/`; 
        await deleteOrganization(url);
    });
});

async function deleteOrganization(url) {
    const result = await Alert.confirmationAlert({
        title: "Eliminar organización",
        text: "¿Está seguro de que desea eliminar esta organización externa?",
        confirmButtonText: "Eliminar",
        cancelButtonText: "Cancelar"
    });

    if (!result.isConfirmed) return;

    try {
        const response = await fetch(url, {
            method: "DELETE",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            credentials: "same-origin"
        });

        if (response.ok) {
            Alert.success("¡Organización eliminada correctamente!");
            setTimeout(() => {
                $('#tabla-organizaciones').DataTable().ajax.reload(null, false);
            }, 1500);
        } else {
            const data = await response.json();
            Alert.error(data.error || "Error al eliminar la organización");
        }
    } catch (err) {
        Alert.error("Error de red. Intenta de nuevo.");
        console.error(err);
    }
}
