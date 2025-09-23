import Alert from "/static/js/modules/Alert.js";
import Loader from "/static/js/modules/Loader.js";
import Modal from "/static/js/modules/Modal.js";
import { cleanContainer } from "/static/js/modules/forms/utils.js";

let lastNitSearchValue = "";

const searchOrgsLoader = document.querySelector("#search-orgs-form .loader")
const searchOrgsResult = document.querySelector("#search-orgs-form .form__results")
const searchOrgsSuggest = document.querySelector("#search-orgs-form .form__suggest")

function toggleSearchState(loader, result) {
    Loader.toggleLoader(loader);
    Modal.toggleResultsVisibility(result);
}

export async function handleOrgsFormSubmit(e) {
    e.preventDefault();

    const searchInputValue = e.target.nit.value;
    if (searchInputValue.trim() === "") {
        Alert.error(`El campo de busqueda es obligatorio`);
        return;
    }
    if (searchInputValue == lastNitSearchValue) return;

    lastNitSearchValue = searchInputValue;

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

        const { organizaciones, message, messageType } = json;

        if (messageType === "info") {
            Alert.info(message);
            setTimeout(() => {
                Loader.toggleLoader(searchOrgsLoader);
                searchOrgsSuggest.classList.remove("hide")
            }, 1500);
            return;
        }

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

        const org = json.organizacion;
        document.getElementById("organizacion-nit").textContent = org.nit;
        document.getElementById("organizacion-nombre").textContent = org.nombre;
        document.getElementById("organizacion-representante").textContent = org.representanteLegal;
        document.getElementById("organizacion-telefono").textContent = org.telefono;
        document.getElementById("organizacion-ubicacion").textContent = org.ubicacion;
        document.getElementById("organizacion-sector").textContent = org.sectorEconomico;
        document.getElementById("organizacion-actividad").textContent = org.actividadPrincipal;
    } catch (err) {
        console.error(err);
        Alert.error("Error de red al cargar datos de la organización.");
    }
}

function displayOrganizationsCards(resultContainer, organizations){
    cleanContainer(resultContainer)

    organizations.forEach(organization => {
        const { idOrganizacion, nit, nombre } = organization;

        const organizationCard = document.createElement("DIV")
        organizationCard.classList.add("organization__card");

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

        const viewMoreBtn = document.createElement("A");
        viewMoreBtn.classList.add("organization__btn")
        viewMoreBtn.innerHTML = "<label for='step2'>Visualizar datos</label>"
        viewMoreBtn.onclick = () => getExternalOrganization(idOrganizacion);

        organizationCard.appendChild(organizationInfo)
        organizationCard.appendChild(viewMoreBtn)

        resultContainer.appendChild(organizationCard)
    });
}
