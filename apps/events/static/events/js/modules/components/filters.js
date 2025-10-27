const mapping = {
  "all": "",
  "borradores": "Borrador",
  "enviados": "Enviado",
  "aprobados": "Aprobado",
  "rechazados": "Rechazado"
};

const searchInput = document.querySelector('#events-search-input');
const searchBy = document.querySelector('#events-search-by');

const urlParams = new URLSearchParams(window.location.search);
const currentStatus = urlParams.get('status') || '';
document.querySelectorAll('.filter__btn').forEach(btn => {
  const token = btn.getAttribute('data-filter');
  const expected = mapping[token] || "";
  if (expected === currentStatus) {
    btn.classList.add('filter__btn--active');
  } else btn.classList.remove('filter__btn--active');
});

//* Event to change the search input type based on the select value
searchBy.addEventListener('change', () => {
    const selected = searchBy.value;
    searchInput.type = selected === 'fecha' ? 'date' : 'text';
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

    if (searchInput && searchInput.value.trim()) {
      url.searchParams.set('search', searchInput.value.trim());
      url.searchParams.set('search_by', searchBy.value || 'nombre');
    } else {
      url.searchParams.delete('search');
      url.searchParams.delete('search_by');
    }

    url.searchParams.set('page', 1);
    window.location.href = url.toString();
}

export function resetFilters() {
    // Remove only search and search_by from the URL (keep status)
    const url = new URL(window.location.href);
    url.searchParams.delete('search');
    url.searchParams.delete('search_by');
    window.location.href = url.toString();
}