import { nitRegex, telefonoRegex } from "/static/js/base.js";
import { modalsConfig } from "/static/js/modules/components/modalsConfig.js";
import { goStep, goToListHandler, skipHandler } from "./modules/components/stepper.js";
import Modal from "/static/js/modules/classes/Modal.js";
import API from "/static/js/modules/classes/API.js";
import { validarFormData, handleFileInputsInfo } from "/static/js/modules/forms/utils.js";
import AssociatedRecords from "./modules/components/associatedRecords.js";
import dataStore from "./modules/dataStore.js";
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

const organizationValidationRules = {
    nit: [
        { check: value => nitRegex.test(value), msg: "El NIT no cumple el formato válido (ej. 12345678-9)" }
        
    ],
    telefono: [
        { check: value => telefonoRegex.test(value), msg: "Teléfono inválido" }
    ]
};

//* Selectors
const mainForm = document.getElementById("main-form");
const fileInputs = document.querySelectorAll('input.input-file');

//* Slide section
const slideSection = document.querySelector(".slide__section");
const openSlideSectionBtn = document.getElementById("crear-organizacion-externa");
const closeSlideSectionBtn = document.getElementById("close-slide-section");
const createOrganizationForm = document.getElementById("crear-organizacion-form");

//* Step sections
const nextStepBtns = document.querySelectorAll(".step__button--next[data-skip]")
const finishStepBtn = document.querySelector(".step__button--finish");

//* Event Listeners
document.addEventListener("DOMContentLoaded", () => {
    if (!window.currentUser) window.location.reload();
    const currentUser = window.currentUser;

    //* Init step form
    goStep(1);

    //* Init modals
    Modal.initModals();

    modalsConfig.forEach(c => {
        Modal.handleSearchFormSubmit({
            formSelector: c.formSelector,
            loaderSelector: c.loaderSelector,
            resultSelector: c.resultSelector,
            suggestSelector: c.suggestSelector,
            endpoint: c.endpoint,
            valueField: c.valueField,
            displayCallback: (container, items) => {
                Modal.displayCards(container, items, c.icon, c.fields, c.modalStepLabel, c.onClickCallback.bind(c));
            }
        });
    });

    //* Others event listeners
    mainForm.addEventListener("submit", handleMainFormSubmit);
    nextStepBtns.forEach(btn => btn.onclick = skipHandler)
    finishStepBtn.onclick = () => goToListHandler("/dashboard/");
    fileInputs.forEach(input => handleFileInputsInfo(input))

    //* Slide section event listeners
    openSlideSectionBtn.addEventListener("click", openSlideSection)
    closeSlideSectionBtn.addEventListener("click", closeSlideSection)
    createOrganizationForm.addEventListener("submit", handleOrganizationFormSubmit)

    //* Load the current user as the default/main organizer
    const assignedOrganizatorsContainer = document.querySelector(".main__step--3 .step__cards");

    const recordUI = {
        nombreCompleto: currentUser.nombreCompleto,
        rol: currentUser.rol
    };

    AssociatedRecords.addRecordToUI(currentUser.id, recordUI, "organizadores", assignedOrganizatorsContainer, true)
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

function openSlideSection() {
    slideSection.classList.add("active")
}

function closeSlideSection() {
    slideSection.classList.remove("active")
}

async function handleOrganizationFormSubmit(e) {
    e.preventDefault();

    // Validate form
    let formData = new FormData(createOrganizationForm);
    if (!validarFormData(formData, organizationValidationRules)) return;

    //Fetch the endpoint
    const result = await API.post("/orgs/api/registro/", formData);
    if (result.error) return;

    Alert.success("Organización registrada exitosamente");
    setTimeout(closeSlideSection, 1500);
}