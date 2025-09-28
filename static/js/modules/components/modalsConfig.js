import AssociatedRecords from "/static/events/js/modules/components/associatedRecords.js";
import Modal from "../classes/Modal.js";

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
        suggestSelector: '#search-instalaciones-form .form__suggest',
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
        buttonId: 'asignar-org-btn',
        modalId: 'modal-organizaciones',
        formSelector: '#search-orgs-form',
        loaderSelector: '#search-orgs-form .loader',
        resultSelector: '#search-orgs-form .form__results',
        suggestSelector: '#search-orgs-form .form__suggest',
        endpoint: '/orgs/api/',
        valueField: 'nit',
        fields: [
            { key: 'nombre', label: 'Nombre', tag: 'H5' },
            { key: 'nit', label: 'NIT' },
            { key: 'sector', label: 'Sector' }
        ],
        icon: 'ri-building-fill',
        stepLabel: 'Visualizar datos',
        //onClickCallback: item => getExternalOrganization(item.idOrganizacion)
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