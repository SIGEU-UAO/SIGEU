import Alert from "/static/js/modules/classes/Alert.js";

export default class Datatable{
    static initDatatable(url){
        $('#tabla-organizaciones').DataTable({
            serverSide: true,
            processing: true,
            ajax: async (data, callback) => {
                try {
                    const urlFetch = new URL(url, window.location.origin);

                    // Añadir parámetros que el servidor espera
                    urlFetch.searchParams.append('draw', data.draw);
                    urlFetch.searchParams.append('start', data.start);
                    urlFetch.searchParams.append('length', data.length);

                    // search puede venir como objeto { value: '...'}
                    const globalSearch = (data.search && data.search.value) ? data.search.value : '';
                    urlFetch.searchParams.append('search[value]', globalSearch);

                    // Si quieres enviar order/columns mínimos, puedes añadirlos así:
                    // (ejemplo: primer order)
                    if (Array.isArray(data.order) && data.order.length) {
                        urlFetch.searchParams.append('order[0][column]', data.order[0].column);
                        urlFetch.searchParams.append('order[0][dir]', data.order[0].dir);
                    }

                    const response = await fetch(urlFetch);
                    const json = await response.json();

                    callback(json);
                } catch (err) {
                    Alert.error("Error cargando organizaciones");
                    callback({ data: [] });
                }
            },
            columns: [
                { data: null, defaultContent: '', orderable: false }, // control column (no data)
                { data: "nit" },
                { data: "nombre" },
                { data: "representanteLegal" },
                { data: "telefono" },
                { data: "ubicacion" },
                { data: "sectorEconomico" },
                {
                    data: "actividadPrincipal",
                    render: (data, type) => 
                        type === "display" && data.length > 30 
                        ? data.slice(0, 50) + "…" 
                        : data
                },
                {
                    data: "esCreador",
                    orderable: false,
                    searchable: false,
                    render: (data, type, row) => {
                        if (data) {
                            return `
                                <a href="/orgs/editar/${row.id}"><i class="ri-pencil-fill"></i></a>
                                <button data-id="${row.id}"><i class="ri-delete-bin-fill"></i></button>
                            `;
                        }
                        return '';
                    }
                }
            ],
            language: {
                url: "https://cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json"
            },
            order: [[1, 'asc']],
            responsive: {
                details: {
                    type: 'column',
                    target: 0,
                }
            },
            columnDefs: [
                { className: 'control', orderable: false, targets: 0 },    // control column (first)
                { responsivePriority: 1, targets: -1 },                    // the last column (Actions) does not collapse
                { responsivePriority: 2, targets: 1 },  // NIT
                { responsivePriority: 3, targets: 2 },  // Nombre
                { responsivePriority: 4, targets: 3 },  // Representante Legal
                { responsivePriority: 5, targets: 4 },  // Teléfono
                { responsivePriority: 6, targets: 5 },  // Ubicación
                { responsivePriority: 7, targets: 6 },  // Sector Económico
                { responsivePriority: 8, targets: 7 }   // Actividad Principal -> la primera en colapsar
            ],
                pageLength: 10,
                lengthMenu: [5, 10, 25, 50]
            });
    }
}