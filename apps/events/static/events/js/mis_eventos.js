import { filterByState, resetFilters, searchByForm } from "./modules/components/filters.js";
import Alert from "/static/js/modules/classes/Alert.js";
import API from "/static/js/modules/classes/API.js"; 

//* Selectors
const cardsContainer = document.querySelector('.cards');
const cards = cardsContainer ? cardsContainer.querySelectorAll('.card') : [];
const noResultsContainer = document.querySelector('.no-results-container');
noResultsContainer.style.display = cards.length === 0 ? 'flex' : 'none';

const searchForm = document.querySelector('#events-search-form');
const filtersResetBtn = document.querySelector('#reset-filters-btn');

//* Event Listeners
document.querySelectorAll('.filters__buttons .filter__btn').forEach(btn => {
  const token = btn.getAttribute('data-filter'); // 'aprobados', 'all', etc.
  btn.addEventListener('click', () => filterByState(token));
});

searchForm.addEventListener('submit', searchByForm)
if (filtersResetBtn) filtersResetBtn.addEventListener("click", resetFilters);

document.addEventListener("click", async (event) => {
    const btn = event.target.closest(".card__btn--send");
    if (!btn) return;

    const id = btn.dataset.id;
    const url = `/eventos/api/enviar-validacion/${id}/`;

    try {
        const result = await Alert.confirmationAlert({
            title: "¿Enviar evento?",
            text: "¿Estás seguro de enviar el evento seleccionado a validación?",
            confirmButtonText: "Enviar",
            cancelButtonText: "Cancelar"
        });

        if (!result.isConfirmed) return;

        const response = await API.post(url);
        if (response.error) {
            Alert.error(response.error);
            return;
        }

        Alert.success("Evento enviado a validación correctamente.");

        setTimeout(() => {
            window.location.reload();
        }, 1500);
    } catch (error) {
        Alert.error("Error al procesar la solicitud");
        console.error(error);
    }
});