import AssociatedRecords from "/static/events/js/modules/components/associatedRecords.js";
import Modal from "../classes/Modal.js";
import API from "../classes/API.js";

// Configuration of all modes
export const modalOpeners = [
    { buttonId: 'asignar-instalacion-btn', modalId: 'modal-instalaciones' },
    { buttonId: 'asignar-organizador-btn', modalId: 'modal-organizadores' },
    { buttonId: 'asignar-organizacion-btn', modalId: 'modal-organizaciones' }
];

export const modalsConfig = [
    {
        buttonId: 'asignar-instalacion-btn',
        modalId: 'modal-instalaciones',
        type: 'instalaciones',
        formSelector: '#search-instalaciones-form',
        loaderSelector: '#search-instalaciones-form .loader',
        resultSelector: '#search-instalaciones-form .form__results',
        endpoint: '/instalaciones/api/',
        valueField: 'ubicacion',
        fields: [
            { key: 'ubicacion', label: 'Ubicacion', tag: 'H5' },
            { key: 'tipo', label: 'Tipo' },
            { key: 'capacidad', label: 'Capacidad' }
        ],
        icon: 'ri-map-fill',
        modalStepLabel: 'Asignar instalación',
        assignedRecordsContainerSelector: ".main__step--2 .step__cards",
        onClickCallback: function(resultContainer, item) {
            AssociatedRecords.addRecord({ id: item["idInstalacion"], ubicacion: item["ubicacion"], tipo: item["tipo"] }, this.type, this.assignedRecordsContainerSelector)
            Modal.closeModal(resultContainer.closest("dialog"))
        }
    },
    {
        buttonId: 'asignar-organizador-btn',
        modalId: 'modal-organizadores',
        type: "organizadores",
        editable: true,
        formSelector: '#search-organizadores-form',
        loaderSelector: '#search-organizadores-form .loader',
        resultSelector: '#search-organizadores-form .form__results',
        endpoint: '/organizadores/api/',
        valueField: 'nombre_completo',
        fields: [
            { key: 'nombre_completo', label: '', tag: 'H5' },
            { key: 'numeroIdentificacion', label: 'Número identificación' },
            { key: 'rol', label: 'Rol' }
        ],
        icon: 'ri-map-pin-user-fill',
        modalStepLabel: 'Visualizar datos',
        assignedRecordsContainerSelector: ".main__step--3 .step__cards",
        onClickCallback: async function(resultContainer, item) {
            const modal = resultContainer.closest("dialog")
            const result = await API.fetchGet(`/organizadores/api/${item.idUsuario}`)
            if (result.error) return; 
            Modal.renderDetailStep(modal, result.data.organizador, this.type)
            Modal.goStep(modal, "next");
        },
        associateFormSelector: "#asociar-organizador-form",
        associateValidationRules: {
            id: [{ check: (val) => !isNaN(Number(val)) && Number(val) > 0, msg: "El ID debe ser un número válido mayor que 0"}],
            aval: [{ check: (val) => val instanceof File && val.name.endsWith('.pdf'), msg: "Debes subir un archivo PDF"}]
        },
        fieldsRecordUI: ["rol"]
    },
    {
        buttonId: 'asignar-organizacion-btn',
        modalId: 'modal-organizaciones',
        type: "organizaciones",
        editable: true,
        formSelector: '#search-organizaciones-form',
        loaderSelector: '#search-organizaciones-form .loader',
        resultSelector: '#search-organizaciones-form .form__results',
        suggestSelector: '#search-organizaciones-form .form__suggest',
        endpoint: '/orgs/api/',
        valueField: 'nit',
        fields: [
            { key: 'nit', label: 'NIT', tag: 'H5' },
            { key: 'nombre', label: 'Nombre' },
            { key: 'representanteLegal', label: 'Representante Legal' }
        ],
        icon: 'ri-map-pin-user-fill',
        modalStepLabel: 'Visualizar datos',
        assignedRecordsContainerSelector: ".main__step--4 .step__cards",
        onClickCallback: async function(resultContainer, item) {
            const modal = resultContainer.closest("dialog")
            const result = await API.fetchGet(`/orgs/api/${item.idOrganizacion}`)
            if (result.error) return; 
            Modal.renderDetailStep(modal, result.data.organizacion, this.type)
            Modal.goStep(modal, "next");
        },
        associateFormSelector: "#asociar-organizacion-form",
        associateValidationRules: {
            id: [{ check: (val) => !isNaN(Number(val)) && Number(val) > 0, msg: "El ID debe ser un número válido mayor que 0"}],
            certificado_participacion: [{ check: (val) => val instanceof File && val.name.endsWith('.pdf'), msg: "Debes subir un archivo PDF"}]
        },
        fieldsRecordUI: ["nit", "nombre"]
    }
];