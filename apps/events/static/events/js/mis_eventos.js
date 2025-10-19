import { filterByState, resetFilters, searchByForm } from "./modules/components/filters.js";

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