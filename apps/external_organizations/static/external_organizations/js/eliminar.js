import API from "/static/js/modules/classes/API.js";

const title = "Eliminar organización";
const text = "¿Está seguro de que desea eliminar esta organización externa?";
const successText = "¡Organización eliminada correctamente!";
const errorText = "Error al eliminar la organización"
const datatableId = "tabla-organizaciones"

document.addEventListener("DOMContentLoaded", () => {
    document.addEventListener("click", async (event) => {
        const btn = event.target.closest("button[data-id]");
        if (!btn) return;

        const id = btn.dataset.id;
        const url = `/orgs/api/delete/${id}/`; 
        await API.delete(url, title, text, successText, errorText, datatableId);
    });
});

