import Alert from "/static/js/modules/Alert.js";
import Loader from "/static/js/modules/Loader.js";
import Modal from "/static/js/modules/Modal.js";
import { cleanContainer } from "/static/js/modules/forms/utils.js";

//* Selectores
const searchOrgsLoader = document.querySelector("#search-orgs-form .loader")
const searchOrgsResult = document.querySelector("#search-orgs-form .form__results")
const searchOrgsSuggest = document.querySelector("#search-orgs-form .form__suggest")

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

    searchOrgsResult.classList.add("hide");
    searchOrgsSuggest.classList.add("hide");
    Loader.toggleLoader(searchOrgsLoader);

    try {
        let res = await fetch(`/orgs/api/?nit=${searchInputValue}`);
        let json = await res.json();
        if (!res.ok) {
            Alert.error(json.error || "Error en el registro");
            setTimeout(() => toggleSearchState(searchOrgsLoader, searchOrgsResult), 1500);
            return;   
        }

        //* Display cards with organizations
        const { organizaciones, message, messageType } = json;

        // If there are no organizations, display message and return
        if (messageType === "info") {
            Alert.info(message);
            setTimeout(() => {
                Loader.toggleLoader(searchOrgsLoader);
                searchOrgsSuggest.classList.remove("hide")
            }, 1500);
            return;
        }

        //* Show organizations & alert
        displayOrganizationsCards(searchOrgsResult, organizaciones);
        Alert.success(message)
        toggleSearchState(searchOrgsLoader, searchOrgsResult);
    } catch (err) {
        Alert.error("Error de red. Intenta de nuevo.", err);
        console.error(err);
    }
}

export async function getExternalOrganization(id){
    try {
        let res = await fetch(`/orgs/api/${id}/`);
        let json = await res.json();

        if (!res.ok) {
            Alert.error(json.error || "No se pudo obtener la organización");
            return;
        }

        const { nit, nombre, representanteLegal, telefono, ubicacion, sectorEconomico, actividadPrincipal } = json.organizacion;
        nitSpan.textContent = nit;
        nombreSpan.textContent = nombre;
        representanteSpan.textContent = representanteLegal;
        telefonoSpan.textContent = telefono;
        ubicacionSpan.textContent = ubicacion;
        sectorSpan.textContent = sectorEconomico;
        actividadSpan.textContent = actividadPrincipal;
    } catch (err) {
        console.error(err);
        Alert.error("Error de red al cargar datos de la organización.");
    }
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
