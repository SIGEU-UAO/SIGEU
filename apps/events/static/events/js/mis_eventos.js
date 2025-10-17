document.addEventListener('DOMContentLoaded', () => {
  const mapping = {
    "all": "",
    "borradores": "Borrador",
    "enviados": "Enviado",
    "aprobados": "Aprobado",
    "rechazados": "Rechazado"
  };

  document.querySelectorAll('.filter__btn').forEach(btn => {
    const token = btn.getAttribute('data-filter'); // p.e. "aprobados" o "all"
    btn.addEventListener('click', () => {
      const status = mapping[token] || "";
      const url = new URL(window.location.href);
      if (status) url.searchParams.set('status', status);
      else url.searchParams.delete('status');
      url.searchParams.set('page', 1);
      window.location.href = url.toString();
    });
  });
});

