import { handleFileInputsInfo, validarFormData } from "/static/js/modules/forms/utils.js";
import API from "/static/js/modules/classes/API.js"; 
import Alert from "/static/js/modules/classes/Alert.js";

// ===== Selects ===== //
const infoOrgBtns = document.querySelectorAll(".card__btn--infoOrg");
const infoOrgExtBtns = document.querySelectorAll(".card__btn--infoOrgExt");
const evalBtns = document.querySelectorAll(".card__btn--eval");

// ===== Modals ===== //
const modalOrg = document.getElementById("modal-organizador");
const modalOrgExt = document.getElementById("modal-organizacion-externa");

// ===== Modal Evaluation ===== //
const modalEval = document.getElementById("modal-evaluacion");
const evalForm = document.getElementById("modal-evaluacion-form")
const evalSelectForm = document.getElementById("tipo-evaluacion");
const evalApproveFormSection = document.getElementById("form__approve");
const evalRejectFormSection = document.getElementById("form__reject");
const evalActaInput = document.getElementById("acta-aprobacion");
const evalJustificationInput = document.getElementById("justificacion");

// ===== Cards ===== //
const cardsContainer = document.querySelector('.cards');
const cards = cardsContainer ? cardsContainer.querySelectorAll('.card') : [];
const noResultsContainer = document.querySelector('.no-results-container');
noResultsContainer.style.display = cards.length === 0 ? 'flex' : 'none';

// ===== References ModalOrganizador ===== //
const nombreOrg = modalOrg?.querySelector(".nombreOrg");
const rolOrg = modalOrg?.querySelector(".rolOrg");
const correoOrg = modalOrg?.querySelector(".correoOrg");
const telefonoOrg = modalOrg?.querySelector(".telefonoOrg");
const identificacionOrg = modalOrg?.querySelector(".identificacionOrg");
const tipoAvalOrg = modalOrg?.querySelector(".tipoAvalOrg");
const avalBtnOrg = modalOrg?.querySelector(".modal__aval-btn");

// ===== References ModalOrganizacionesExternas ===== //
const nombreExt = modalOrgExt?.querySelector(".nombreOrgExt");

const nitExt = modalOrgExt?.querySelector(".nitOrgExt");
const sectorExt = modalOrgExt?.querySelector(".sectorOrgExt");
const actividadExt = modalOrgExt?.querySelector(".actividadOrgExt");
const representanteExt = modalOrgExt?.querySelector(".representanteOrgExt");

const telefonoExt = modalOrgExt?.querySelector(".telefonoOrgExt");
const ubicacionExt = modalOrgExt?.querySelector(".ubicacionOrgExt");
const certBtnExt = modalOrgExt?.querySelector(".modal__cert-btn");

// ===== Events Listeners ===== //
infoOrgBtns.forEach(btn => btn.addEventListener("click", () => openOrganizerModal(modalOrg, btn)));
infoOrgExtBtns.forEach(btn => btn.addEventListener("click", () => openExternalOrganizationModal(modalOrgExt, btn)));

// Evaluation
evalBtns.forEach(btn => btn.addEventListener("click", () => openEvaluationModal(modalEval, btn)));
evalSelectForm.addEventListener("change", () => changeEvalFormSection());
evalForm.addEventListener("submit", e => sendEvaluation(e));
handleFileInputsInfo(evalActaInput);

// === Functions === //
async function openOrganizerModal(modal, btn){
    const data = btn.dataset;
    const orgId = data.orgid;
    const eventId = data.eventid;
    const url = `/organizadores/api/${orgId}/`;
    const urlAval = `/eventos/api/obtener-datos-organizador/${eventId}/${orgId}/`

    try {
      // API calls //
      const response = await API.fetchGet(url);
      const awake = await API.fetchGet(urlAval);

      const org = response.data.organizador;
      const avalData = awake.data.data.organizador_evento;

      // === Modal === //
      nombreOrg.textContent = `${org.nombres} ${org.apellidos}` || "Sin nombre";
      rolOrg.textContent = org.rol || "Sin rol";
      correoOrg.textContent = org.email || "No disponible";
      telefonoOrg.textContent = org.telefono || "No disponible";
      identificacionOrg.textContent = org.numeroIdentificacion || "No disponible";

      if (!avalData) {
        throw new Error("La estructura de datos del aval es inválida.");
      }

      tipoAvalOrg.textContent = avalData.tipo || "No aplica";

      if (avalData.aval) {
        avalBtnOrg.href = avalData.aval;
        avalBtnOrg.style.display = "inline-flex";
      } else {
        avalBtnOrg.style.display = "none";
      }

      // === Show Modal === //
      modalOrg.showModal();

    } catch (error) {
      console.error("Error al cargar el organizador:", error);
    }
}

async function openExternalOrganizationModal(modal, btn){
  const data = btn.dataset;
    const orgIdExt = data.orgextid;
    const eventId = data.eventoid;

    const urlOrg = `/orgs/api/${orgIdExt}/`;
    const urlInv = `/eventos/api/obtener-datos-organizacion-invitada/${eventId}/${orgIdExt}/`;

    try {
      //API calls//
      const orgResponse = await API.fetchGet(urlOrg);  
      const invResponse = await API.fetchGet(urlInv);

      const inv = invResponse.data.data.OrganizacionInvitada;
      const org = orgResponse.data.organizacion;

      // === Modal === //
      nombreExt.textContent = org.nombre || "Sin nombre";
      nitExt.textContent = org.nit || "Sin NIT";
      telefonoExt.textContent = org.telefono || "No disponible";
      ubicacionExt.textContent = org.ubicacion || "No disponible";
      actividadExt.textContent = org.actividadPrincipal || "No disponible";
      sectorExt.textContent = org.sectorEconomico || "No disponible";

      if (inv.representante_asiste==false){
        representanteExt.textContent = inv.representante_alterno || "No aplica";
      }else{
        representanteExt.textContent = org.representanteLegal || "No disponible";
      }

      if (inv.certificado_participacion) {
        certBtnExt.href = inv.certificado_participacion;
        certBtnExt.style.display = "inline-flex";
      } else {
        certBtnExt.style.display = "none";
      }

      // === Show Modal === //
      modalOrgExt.showModal();

    } catch (error) {
      console.error("Error al cargar la organización externa:", error);
      alert("No se pudo cargar la información de la organización externa.");
    }
}

// === Evaluation Modal === //
function openEvaluationModal(modal, btn){
    const data = btn.dataset;
    const eventId = data.eventoid;
    evalForm.dataset.eventId = eventId;
    modal.showModal();
}

// Change eval form section
function changeEvalFormSection() {
    if (evalSelectForm.value === "aprobacion") {
        evalApproveFormSection.style.display = "flex";
        evalRejectFormSection.style.display = "none";
        
        // Disable justification and enable acta
        evalJustificationInput.disabled = true;
        evalActaInput.disabled = false;
    } else {
        evalApproveFormSection.style.display = "none";
        evalRejectFormSection.style.display = "flex";
        
        // Enable justification and disable acta
        evalJustificationInput.disabled = false;
        evalActaInput.disabled = true;
    }
}

// TODO: Send evaluation
async function sendEvaluation(e) {
    e.preventDefault();
    const eventId = evalForm.dataset.eventId;
    const data = new FormData(evalForm);
    if (!validarFormData(data)) {
      modalEval.close();
      return;
    };

    // Validate act approval extension (must be .pdf)
    if (data.get("acta-aprobacion") && !data.get("acta-aprobacion").name.endsWith(".pdf")) {
      Alert.error("El archivo de la acta de aprobación debe ser un PDF");
      modalEval.close();
      return;
    }

    // List form data
    for (const [key, value] of data.entries()) {
      console.log(`${key}: ${value}`);
    }
}