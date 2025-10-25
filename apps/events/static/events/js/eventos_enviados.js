import { modalsConfig } from "/static/js/modules/components/modalsConfig.js";
import Modal from "/static/js/modules/classes/Modal.js";
import API from "/static/js/modules/classes/API.js";


const infoOrgBtns = document.querySelectorAll(".card__btn--infoOrg");
const modal = document.getElementById("modal-organizadores");
const closeBtn = modal.querySelector(".modal__close");


infoOrgBtns.forEach(btn => btn.addEventListener("click", async () => {
    const organizadorId = btn.dataset.organizador-id;
    const eventoId = btn.dataset.evento-id;

    try {
        const url = `/eventos/api/obtener-detalles-organizador/${organizadorId}/${eventoId}/`;
        const response = await API.get(url);

        if (response.ok) {
            const data = await response.json();
            // Aquí puedes actualizar el contenido del modal con los datos del organizador
            modal.querySelector(".modal__content").innerHTML = `
                <h2>${data.nombre}</h2>
                <p>${data.descripcion}</p>
            `;
        } else {
            console.error("Error al obtener detalles del organizador");
        }
    } catch (error) {
        console.error("Error en la solicitud:", error);
    }

    modal.showModal();


    // Cerrar al presionar botón ×
    closeBtn.addEventListener("click", () => modal.close());

    // Cerrar al hacer clic fuera del contenido
    modal.addEventListener("click", e => {
        const rect = modal.querySelector(".modal__content").getBoundingClientRect();
        const isInDialog = (
            e.clientX >= rect.left &&
            e.clientX <= rect.right &&
            e.clientY >= rect.top &&
            e.clientY <= rect.bottom
        );
        if (!isInDialog) modal.close();
    });
}));
