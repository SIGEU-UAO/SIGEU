import { handleOrgsFormSubmit } from "/static/external_organizations/js/components/modal.js";
import Modal from "/static/js/modules/classes/Modal.js";
import { validarFormData } from "/static/js/modules/forms/utils.js";
import Alert from "/static/js/modules/classes/Alert.js";
import API from "/static/js/modules/classes/API.js";

//* Variables
const validationRules = {
    fecha: [
        {check:value=>{if(!value) return false;const[yy,mm,dd]=value.split('-').map(Number);const f=new Date(yy,mm-1,dd);const h=new Date();h.setHours(0,0,0,0);return f.getTime()>=h.getTime()},msg:"La fecha debe ser hoy o posterior"}
    ],
    horaFin: [
        {check:(value,formData)=>{const p=s=>{if(!s) return NaN;const[a='0',b='0',c='0']=s.trim().split(':');return Number(a)*3600+Number(b)*60+Number(c)};return p(value)>p(formData.get("horaInicio"))},msg:"La hora fin debe ser mayor a la hora inicio"}
    ],
};

let eventoID;

//* Selectors
const mainForm = document.getElementById("main-form");
const modals = document.querySelectorAll('.modal');

//* Steps radios
const step1 = document.querySelector("#step1");
const step2 = document.querySelector("#step2");
const step3 = document.querySelector("#step3");

//* Associate organizations modals
const searchOrgsForm = document.getElementById("search-orgs-form");

//* Event Listeners
mainForm.addEventListener("submit", handleSubmit);
//modals.forEach(modal => modal.querySelectorAll('.modal__close').forEach(btn => btn.addEventListener("click", e => Modal.closeModal(modal))))
//searchOrgsForm.addEventListener("submit", handleOrgsFormSubmit)

//* Functions
async function handleSubmit(e) {
    e.preventDefault();

    // Validate form
    let formData = new FormData(mainForm);
    if (!validarFormData(formData, validationRules)) return;

    //Fetch the endpoint
    const result = await API.post("/eventos/api/registro/", formData);
    if (result.error) return;

    Alert.success("Evento registrado en estado borrador");
    eventoID = result.data.evento; //Get the event id
    step1.checked = false;
    step2.checked = true;
    mainForm.reset();
}