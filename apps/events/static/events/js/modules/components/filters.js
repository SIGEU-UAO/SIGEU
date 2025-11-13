import Alert from "/static/js/modules/classes/Alert.js";

const mapping = {
  "all": "",
  "borradores": "Borrador",
  "enviados": "Enviado",
  "aprobados": "Aprobado",
  "rechazados": "Rechazado"
};

const minDate = new Date().toISOString().split('T')[0];

const searchInput = document.querySelector('#events-search-input');
const searchBy = document.querySelector('#events-search-by');
const searchInputEndDateContainer = document.querySelector('.form__group:has(#events-search-input-endate)');
const searchInputEndDate = document.querySelector('#events-search-input-endate');

const urlParams = new URLSearchParams(window.location.search);
const currentStatus = urlParams.get('status') || '';
const currentSearch = urlParams.get('search') || '';
const currentSearchBy = urlParams.get('search_by') || '';
const currentSearchEndDate = urlParams.get('search_end') || '';

document.querySelectorAll('.filter__btn').forEach(btn => {
  const token = btn.getAttribute('data-filter');
  const expected = mapping[token] || "";
  if (expected === currentStatus) {
    btn.classList.add('filter__btn--active');
  } else btn.classList.remove('filter__btn--active');
});

//*  Display the latest filter in the text fields according to the URL
if(currentSearch !== '') searchInput.value = currentSearch;
if(currentSearchBy !== '') searchBy.value = currentSearchBy;
if(currentSearchBy === 'fecha') {
    searchInput.type = 'date';
    searchInput.min = minDate;
    searchInputEndDateContainer.classList.remove('form__group--hidden');
    searchInputEndDate.min = minDate;
    searchInput.previousElementSibling.classList.remove('form__label--hidden');
}
if(currentSearchEndDate !== '') searchInputEndDate.value = currentSearchEndDate;

//* Event to change the search input type based on the select value
searchBy.addEventListener('change', () => {
    const selected = searchBy.value;
    searchInput.type = selected === 'fecha' ? 'date' : 'text';

    if (selected === 'fecha') {
        searchInput.min = minDate;
        searchInputEndDateContainer.classList.remove('form__group--hidden');
        searchInputEndDate.min = minDate;
        searchInput.previousElementSibling.classList.remove('form__label--hidden');
    } else {
        searchInputEndDateContainer.classList.add('form__group--hidden');
        searchInputEndDate.min = "";
        searchInput.previousElementSibling.classList.add('form__label--hidden');
    }
})

export function filterByState(token) {
    const status = mapping[token] || "";
    const url = new URL(window.location.href);
    if (status) url.searchParams.set('status', status);
    else url.searchParams.delete('status');
    url.searchParams.set('page', 1);

    // keep current search in inputs
    if (searchInput && searchInput.value.trim()) {
      url.searchParams.set('search', searchInput.value.trim());
      if (searchBy && searchBy.value) url.searchParams.set('search_by', searchBy.value);
    } else {
      url.searchParams.delete('search');
      url.searchParams.delete('search_by');
    }

    window.location.href = url.toString();
}

export function searchByForm(e) {
    e.preventDefault();
    const url = new URL(window.location.href);
    const searchValue = searchInput?.value.trim();
    const searchEndDateValue = searchInputEndDate?.value.trim();
    const searchByValue = searchBy?.value || 'nombre';

    if (searchValue || searchEndDateValue) {
        // Handle date range validation
        if (searchByValue === 'fecha') {
            const startDate = new Date(searchValue);
            const endDate = new Date(searchEndDateValue);
            
            if (endDate && endDate < startDate) {
                Alert.error('La fecha de fin debe ser mayor o igual a la fecha de inicio');
                return; // Stop execution if validation fails
            }
            
            // Set both start and end date parameters
            url.searchParams.set('search', searchValue);
            if (endDate) {
                url.searchParams.set('search_end', searchEndDateValue);
            } else {
                url.searchParams.delete('search_end');
            }
        } else {
            // Handle regular search
            url.searchParams.set('search', searchValue);
            url.searchParams.delete('search_end');
        }
        url.searchParams.set('search_by', searchByValue);
    } else {
        // Clear all search parameters if no search value
        url.searchParams.delete('search');
        url.searchParams.delete('search_by');
        url.searchParams.delete('search_end');
    }

    url.searchParams.set('page', 1);
    window.location.href = url.toString();
}

export function resetFilters() {
    // Remove only search and search_by from the URL (keep status)
    const url = new URL(window.location.href);
    url.searchParams.delete('search');
    url.searchParams.delete('search_by');
    url.searchParams.delete('search_end');
    window.location.href = url.toString();
}