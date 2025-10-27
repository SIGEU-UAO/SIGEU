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
const sendBtns = document.querySelectorAll(".card__btn--send")
const deleteBtns = document.querySelectorAll(".card__btn--delete");

//* Event Listeners
document.querySelectorAll('.filters__buttons .filter__btn').forEach(btn => {
  const token = btn.getAttribute('data-filter'); // 'aprobados', 'all', etc.
  btn.addEventListener('click', () => filterByState(token));
});

searchForm.addEventListener('submit', searchByForm)
if (filtersResetBtn) filtersResetBtn.addEventListener("click", resetFilters);

sendBtns.forEach(btn => btn.addEventListener('click', async () => {

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

        const response = await API.patch(url);
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
}));

deleteBtns.forEach(btn => btn.addEventListener('click', async () => {
    const id = btn.dataset.id;
    if (!id) {
      Alert.error("No se encontró el id del evento. Recarga e inténtalo de nuevo.");
      return;
    }
    const url = `/eventos/api/eliminar/${id}/`;

    try {
      await API.delete(
        url,
        "Eliminar evento",
        "Esta acción eliminará el evento y sus archivos asociados. ¿Deseas continuar?",
        "Evento eliminado correctamente.",
        "No se pudo eliminar el evento.",
        null
      );

      setTimeout(() => {
        window.location.reload();
      }, 1500);

    } catch (err) {
      Alert.error("Error al procesar la solicitud.");
    }
  }));