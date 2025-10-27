import API from "/static/js/modules/classes/API.js"; 

// ===== Selects ===== //
const infoOrgBtns = document.querySelectorAll(".card__btn--infoOrg");
const infoOrgExtBtns = document.querySelectorAll(".card__btn--infoOrgExt");

const modalOrg = document.getElementById("modal-organizador");
const modalOrgExt = document.getElementById("modal-organizacion-externa");

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

// ==== ORGANIZADOR ==== //
infoOrgBtns.forEach(btn => {
  btn.addEventListener("click", async () => {
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
  });
});

// ==== ORGANIZACIONES EXTERNAS ==== //
infoOrgExtBtns.forEach(btn => {
  btn.addEventListener("click", async () => {
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
  });
});