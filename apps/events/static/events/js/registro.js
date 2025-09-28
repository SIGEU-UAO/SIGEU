import { modalsConfig } from "/static/js/modules/components/modalsConfig.js";
import { goStep } from "./modules/components/stepper.js";
import Modal from "/static/js/modules/classes/Modal.js";
import API from "/static/js/modules/classes/API.js";
import dataStore from "./modules/dataStore.js";
import AssociatedRecords from "./modules/components/associatedRecords.js";
import { validarFormData } from "/static/js/modules/forms/utils.js";
import Alert from "/static/js/modules/classes/Alert.js";

//* Variables
const validationRules = {
    fecha: [
        {check:value=>{if(!value) return false;const[yy,mm,dd]=value.split('-').map(Number);const f=new Date(yy,mm-1,dd);const h=new Date();h.setHours(0,0,0,0);return f.getTime()>=h.getTime()},msg:"La fecha debe ser hoy o posterior"}
    ],
    horaFin: [
        {check:(value,formData)=>{const p=s=>{if(!s) return NaN;const[a='0',b='0',c='0']=s.trim().split(':');return Number(a)*3600+Number(b)*60+Number(c)};return p(value)>p(formData.get("horaInicio"))},msg:"La hora fin debe ser mayor a la hora inicio"}
    ],
};

//* Selectors
const mainForm = document.getElementById("main-form");
const modals = document.querySelectorAll('.modal');

//* Steps buttons
const nextStepButtons = document.querySelectorAll(".step__button--next")

//* Event Listeners
document.addEventListener("DOMContentLoaded", () => {
    //* Init step form
    goStep(1);

    //* Init modals
    Modal.initModals(modalsConfig.map(c => ({ buttonId: c.buttonId, modalId: c.modalId })));

    modalsConfig.forEach(c => {
        Modal.handleSearchFormSubmit({
            formSelector: c.formSelector,
            loaderSelector: c.loaderSelector,
            resultSelector: c.resultSelector,
            suggestSelector: c.suggestSelector,
            endpoint: c.endpoint,
            valueField: c.valueField,
            displayCallback: (container, items) => {
                Modal.displayCards(container, items, c.icon, c.fields, c.stepLabel, c.onClickCallback);
            }
        });
    });

    //* Others add event listeners
    nextStepButtons.forEach(button => button.addEventListener("click", () => goStep("next")))
    mainForm.addEventListener("submit", handleMainFormSubmit);

    //* Events listeners to associate records to the DB
    const associatePhysicalInstallationsBtn = nextStepButtons[0];
    
    if (!associatePhysicalInstallationsBtn.dataset.skip) associatePhysicalInstallationsBtn.addEventListener("click", () => AssociatedRecords.saveDBRecords("/eventos/api/asignar-instalaciones/", "instalaciones"))
});

//* Functions
async function handleMainFormSubmit(e) {
    e.preventDefault();

    // Validate form
    let formData = new FormData(mainForm);
    if (!validarFormData(formData, validationRules)) return;

    //Fetch the endpoint
    const result = await API.post("/eventos/api/registro/", formData);
    if (result.error) return;

    Alert.success("Evento registrado en estado borrador");
    dataStore.eventoId = result.data.evento; // Save the event ID
    goStep("next")
    mainForm.reset();
}