// ===== Selecciones =====
const infoOrgBtns = document.querySelectorAll(".card__btn--infoOrg");
const infoOrgExtBtns = document.querySelectorAll(".card__btn--infoOrgExt");

const modalOrg = document.getElementById("modal-organizador");
const modalOrgExt = document.getElementById("modal-organizacion-externa");

// ===== Referencias dentro del modal de organizador =====
const nombreOrg = modalOrg?.querySelector(".nombreOrg");
const rolOrg = modalOrg?.querySelector(".rolOrg");
const correoOrg = modalOrg?.querySelector(".correoOrg");
const telefonoOrg = modalOrg?.querySelector(".telefonoOrg");
const identificacionOrg = modalOrg?.querySelector(".identificacionOrg");
const tipoAvalOrg = modalOrg?.querySelector(".tipoAvalOrg");
const avalBtnOrg = modalOrg?.querySelector(".modal__aval-btn");

// ===== Referencias dentro del modal de organización externa =====
const nombreExt = modalOrgExt?.querySelector(".nombreOrgExt");

const nitExt = modalOrgExt?.querySelector(".nitOrgExt");
const sectorExt = modalOrgExt?.querySelector(".sectorOrgExt");
const actividadExt = modalOrgExt?.querySelector(".actividadOrgExt");
const representanteExt = modalOrgExt?.querySelector(".representanteOrgExt");

const telefonoExt = modalOrgExt?.querySelector(".telefonoOrgExt");
const ubicacionExt = modalOrgExt?.querySelector(".ubicacionOrgExt");
const certBtnExt = modalOrgExt?.querySelector(".modal__cert-btn");

// ==== ORGANIZADORES INTERNOS ====
infoOrgBtns.forEach(btn => {
  btn.addEventListener("click", () => {
    const data = btn.dataset;

    // Rellenar el modal con los datos
    nombreOrg.textContent = data.nombre || "Sin nombre";
    rolOrg.textContent = data.rol || "Sin rol";
    correoOrg.textContent = data.correo || "No disponible";
    telefonoOrg.textContent = data.telefono || "No disponible";
    identificacionOrg.textContent = data.identificacion || "No disponible";
    tipoAvalOrg.textContent = data.tipoaval || "No especificado";

    // Configurar botón del AVAL
    if (data.avalUrl) {
      avalBtnOrg.href = data.avalUrl;
      avalBtnOrg.style.display = "inline-flex";
    } else {
      avalBtnOrg.style.display = "none";
    }

    // Mostrar el modal
    modalOrg.showModal();
  });
});

// ==== ORGANIZACIONES EXTERNAS ====
infoOrgExtBtns.forEach(btn => {
  btn.addEventListener("click", () => {
    const data = btn.dataset;

    // Rellenar el modal con los datos
    nombreExt.textContent = data.nombre || "Sin nombre";

    nitExt.textContent = data.nit || "Sin NIT";
    sectorExt.textContent = data.sector || "No especificado";
    actividadExt.textContent = data.actividad || "No especificado";

    if (!data.representantealterno || data.representantealterno === "None") {
      representanteExt.textContent = data.representante || "No disponible";
    } else {
      representanteExt.textContent = data.representantealterno || "No disponible";
    }


    telefonoExt.textContent = data.telefono || "No disponible";
    ubicacionExt.textContent = data.ubicacion || "No disponible";

    // Configurar botón del certificado
    if (data.certificadoUrl) {
      certBtnExt.href = data.certificadoUrl;
      certBtnExt.style.display = "inline-flex";
    } else {
      certBtnExt.style.display = "none";
    }

    // Mostrar el modal
    modalOrgExt.showModal();
  });
});