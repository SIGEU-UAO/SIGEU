import Alert from "/static/js/modules/classes/Alert.js";
import Loader from "/static/js/modules/classes/Loader.js";
import Modal from "/static/js/modules/classes/Modal.js";
import API from "/static/js/modules/classes/API.js";
import { cleanContainer } from "/static/js/modules/forms/utils.js";

//* Selectores
const searchOrgsLoader = document.querySelector("#search-orgs-form .loader")
const searchOrgsResult = document.querySelector("#search-orgs-form .form__results")
const searchOrgsSuggest = document.querySelector("#search-orgs-form .form__suggest")

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