// static/events/js/mis_eventos.js
document.addEventListener('DOMContentLoaded', () => {
  const mapping = {
    "all": "",
    "borradores": "Borrador",
    "enviados": "Enviado",
    "aprobados": "Aprobado",
    "rechazados": "Rechazado"
  };

  // filtros por estado (botones)
  document.querySelectorAll('.filter__btn').forEach(btn => {
    const token = btn.getAttribute('data-filter'); // 'aprobados', 'all', etc.
    btn.addEventListener('click', () => {
      const status = mapping[token] || "";
      const url = new URL(window.location.href);
      if (status) url.searchParams.set('status', status);
      else url.searchParams.delete('status');

      // eliminar page (resetear)
      url.searchParams.set('page', 1);

      // conservar búsqueda actual en inputs
      const searchInput = document.querySelector('#events-search-input');
      const searchBy = document.querySelector('#events-search-by');
      if (searchInput && searchInput.value.trim()) {
        url.searchParams.set('search', searchInput.value.trim());
        if (searchBy && searchBy.value) url.searchParams.set('search_by', searchBy.value);
      } else {
        url.searchParams.delete('search');
        url.searchParams.delete('search_by');
      }

      window.location.href = url.toString();
    });
  });

  // búsqueda por nombre/fecha (form)
  const searchForm = document.querySelector('#events-search-form');
  if (searchForm) {
    searchForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const input = document.querySelector('#events-search-input');
      const by = document.querySelector('#events-search-by');
      const url = new URL(window.location.href);

      if (input && input.value.trim()) {
        url.searchParams.set('search', input.value.trim());
        url.searchParams.set('search_by', by.value || 'nombre');
      } else {
        url.searchParams.delete('search');
        url.searchParams.delete('search_by');
      }

      // mantener status si existe (no lo tocamos)
      url.searchParams.set('page', 1);
      window.location.href = url.toString();
    });
  }

  // mostrar mensaje bonito si no hay resultados (después de que el servidor haya renderizado)
  const cardsContainer = document.querySelector('.cards');
  const cards = cardsContainer ? cardsContainer.querySelectorAll('.card') : [];
  const noResultsContainer = document.querySelector('.no-results-container');

  if (cards.length === 0 && noResultsContainer) {
    noResultsContainer.style.display = 'flex'; // o block según tu CSS
  } else if (noResultsContainer) {
    noResultsContainer.style.display = 'none';
  }

  // Marcar botón activo según status en querystring
  const urlParams = new URLSearchParams(window.location.search);
  const currentStatus = urlParams.get('status') || '';
  document.querySelectorAll('.filter__btn').forEach(btn => {
    const token = btn.getAttribute('data-filter');
    const expected = mapping[token] || "";
    if (expected === currentStatus) {
      btn.classList.add('filter__btn--active');
    } else btn.classList.remove('filter__btn--active');
  });
});


