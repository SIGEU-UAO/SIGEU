import { handleOrgsFormSubmit } from "/static/external_organizations/js/components/modal.js";
import Modal from "/static/js/modules/Modal.js";

//* Selectors
const modals = document.querySelectorAll('.modal');

//* Modal de buscar organizacion
const searchOrgsForm = document.getElementById("search-orgs-form");

//* Event Listeners
modals.forEach(modal => modal.querySelectorAll('.modal__close').forEach(btn => btn.addEventListener("click", e => Modal.closeModal(modal))))
searchOrgsForm.addEventListener("submit", handleOrgsFormSubmit)