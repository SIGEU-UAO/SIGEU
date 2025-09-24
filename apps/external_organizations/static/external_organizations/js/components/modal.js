import Alert from "/static/js/modules/classes/Alert.js";
import Loader from "/static/js/modules/classes/Loader.js";
import Modal from "/static/js/modules/classes/Modal.js";
import API from "/static/js/modules/classes/API.js";
import { cleanContainer } from "/static/js/modules/forms/utils.js";

//* Selectores
const searchOrgsLoader = document.querySelector("#search-orgs-form .loader")
const searchOrgsResult = document.querySelector("#search-orgs-form .form__results")
const searchOrgsSuggest = document.querySelector("#search-orgs-form .form__suggest")

//Steps
const step1 = document.querySelector("#step1");
const step2 = document.querySelector("#step2");
const step3 = document.querySelector("#step3");

//* Step-2
const nitSpan = document.getElementById("organizacion-nit");
const nombreSpan = document.getElementById("organizacion-nombre");
const representanteSpan = document.getElementById("organizacion-representante");
const telefonoSpan = document.getElementById("organizacion-telefono");
const ubicacionSpan = document.getElementById("organizacion-ubicacion");
const sectorSpan = document.getElementById("organizacion-sector");
const actividadSpan = document.getElementById("organizacion-actividad");

//* Functions
function toggleSearchState(loader, result) {
    Loader.toggleLoader(loader);
    Modal.toggleResultsVisibility(result);
}

//* Function to search by id
export async function handleOrgsFormSubmit(e) {
    e.preventDefault();

    //Get search value
    const searchInputValue = e.target.nit.value;
    if (searchInputValue.trim() === "") {
        Alert.error(`El campo de busqueda es obligatorio`);
        return;
    }

    //Set default classes
    searchOrgsResult.classList.add("hide");
    searchOrgsSuggest.classList.add("hide");
    Loader.toggleLoader(searchOrgsLoader);

    //Fetch the endpoint
    const result = await API.fetchGet(`/orgs/api/?nit=${searchInputValue}`)
    if (result.error) {
        setTimeout(() => toggleSearchState(searchOrgsLoader, searchOrgsResult), 1500);
        return; 
    }

    //* Display cards with organizations
    const { organizaciones, message, messageType } = result.data; 

    // If there are no organizations, display message and return
    if (messageType === "info") {
        Alert.info(message);
        setTimeout(() => {
            Loader.toggleLoader(searchOrgsLoader);
            searchOrgsSuggest.classList.remove("hide")
        }, 1500);
        return;
    }

    // Show organizations & alert
    displayOrganizationsCards(searchOrgsResult, organizaciones);
    Alert.success(message)
    toggleSearchState(searchOrgsLoader, searchOrgsResult);
}

export async function getExternalOrganization(id){
    //Fetch the endpoint
    const result = await API.fetchGet(`/orgs/api/${id}`)
    if (result.error) {
        step1.checked = true;
        return; 
    }

    const { nit, nombre, representanteLegal, telefono, ubicacion, sectorEconomico, actividadPrincipal } = result.data.organizacion;
    nitSpan.textContent = nit;
    nombreSpan.textContent = nombre;
    representanteSpan.textContent = representanteLegal;
    telefonoSpan.textContent = telefono;
    ubicacionSpan.textContent = ubicacion;
    sectorSpan.textContent = sectorEconomico;
    actividadSpan.textContent = actividadPrincipal;
}

//* Function to display the organizations in the modal
function displayOrganizationsCards(resultContainer, organizations){
    cleanContainer(resultContainer)

    organizations.forEach(organization => {
        const { idOrganizacion, nit, nombre } = organization;

        //* Container div
        const organizationCard = document.createElement("DIV")
        organizationCard.classList.add("organization__card");

        //* Left div
        const organizationInfo = document.createElement("DIV");
        organizationInfo.classList.add("organization__info");

        const organizationIcon = document.createElement("DIV");
        organizationIcon.innerHTML = '<i class="ri-building-fill"></i>'
        organizationIcon.classList.add("organization__icon")

        const organizationDescription = document.createElement("DIV");
        organizationDescription.classList.add("organization__description")

        const organizationName = document.createElement("H5");
        organizationName.textContent = nombre;

        const organizationSector = document.createElement("SPAN");
        organizationSector.textContent = `NIT: ${nit}`;

        organizationDescription.appendChild(organizationName)
        organizationDescription.appendChild(organizationSector)

        organizationInfo.appendChild(organizationIcon)
        organizationInfo.appendChild(organizationDescription)

        //* Right div
        const viewMoreBtn = document.createElement("A");
        viewMoreBtn.classList.add("organization__btn")
        viewMoreBtn.innerHTML = "<label for='step2'>Visualizar datos</label>"
        viewMoreBtn.onclick = () => getExternalOrganization(idOrganizacion);

        //* Append elements
        organizationCard.appendChild(organizationInfo)
        organizationCard.appendChild(viewMoreBtn)

        resultContainer.appendChild(organizationCard)
    });
}
