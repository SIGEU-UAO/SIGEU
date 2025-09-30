import AssociatedRecords from "/static/events/js/modules/components/associatedRecords.js";
import Modal from "../classes/Modal.js";
import API from "../classes/API.js";

// Configuration of all modes
export const modalOpeners = [
    { buttonId: 'asignar-instalacion-btn', modalId: 'modal-instalaciones' },
    { buttonId: 'asignar-organizador-btn', modalId: 'modal-organizadores' }
];

export const modalsConfig = [
    {
        buttonId: 'asignar-instalacion-btn',
        modalId: 'modal-instalaciones',
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
        stepLabel: 'Asignar instalación',
        assignedRecordsContainerSelector: ".main__step--2 .step__cards",
        onClickCallback: function(resultContainer, item) {
            AssociatedRecords.addRecord({ id: item["idInstalacion"], ubicacion: item["ubicacion"], tipo: item["tipo"] }, "instalaciones", this.assignedRecordsContainerSelector)
            Modal.closeModal(resultContainer.closest("dialog"))
        }
    },
    {
        buttonId: 'asignar-organizador-btn',
        modalId: 'modal-organizadores',
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
        stepLabel: 'Visualizar datos',
        assignedRecordsContainerSelector: ".main__step--3 .step__cards",
        onClickCallback: async function(resultContainer, item) {
            const modal = resultContainer.closest("dialog")
            const result = await API.fetchGet(`/organizadores/api/${item.idUsuario}`)
            if (result.error) return; 
            Modal.renderDetailStep(modal, result.data.organizador, "organizadores") // The 1 represents the index of this position in the array, which is used to obtain the modalConfig.
            Modal.goStep(modal, "next");
        },
        associateValidationRules: {
            aval: [{ check: (val) => val instanceof File && val.name, msg: "Debes subir un archivo PDF"}],
            id: [{ check: (val) => !isNaN(Number(val)) && Number(val) > 0, msg: "El ID debe ser un número válido mayor que 0"}]
        },
        extraFormDataFields: ["rol"],
        fieldsRecordUI: ["rol"]
    },
    {
        buttonId: 'asignar-usuario-btn',
        modalId: 'modal-usuarios',
        formSelector: '#search-users-form',
        loaderSelector: '#search-users-form .loader',
        resultSelector: '#search-users-form .form__results',
        suggestSelector: '#search-users-form .form__suggest',
        endpoint: '/usuarios/api/',
        valueField: 'username',
        fields: [
            { key: 'username', label: 'Usuario', tag: 'H5' },
            { key: 'email', label: 'Email' },
            { key: 'rol', label: 'Rol' }
        ],
        icon: 'ri-user-fill',
        stepLabel: 'Seleccionar usuario',
        //onClickCallback: item => selectUser(item)
    }
];