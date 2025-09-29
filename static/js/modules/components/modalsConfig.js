import AssociatedRecords from "/static/events/js/modules/components/associatedRecords.js";
import Modal from "../classes/Modal.js";
import API from "../classes/API.js";

//* Container selectors that store associated/assigned records
const assignedPhysicalInstallationsContainer = document.querySelector(".main__step--2 .step__cards")

// Configuración de todos los modales
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
        onClickCallback: function(resultContainer, item) {
            Modal.closeModal(resultContainer.closest("dialog"))
            AssociatedRecords.addRecord({ id: item["idInstalacion"], annotation: item["tipo"], title: item["ubicacion"], icon: "ri-map-fill", type: "instalaciones" }, assignedPhysicalInstallationsContainer)
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
        onClickCallback: async function(resultContainer, item) {
            const modal = resultContainer.closest("dialog")
            const result = await API.fetchGet(`/organizadores/api/${item.idUsuario}`)
            if (result.error) return; 
            Modal.renderDetailStep(modal, result.data.organizador)
            Modal.goStep(modal, "next");
        }
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