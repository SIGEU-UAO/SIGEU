import dataStore from "../dataStore.js";
import { validateCollection } from "../utils/validations.js";
import { mergeFormDataArray } from "/static/js/modules/forms/utils.js";
import API from "/static/js/modules/classes/API.js";
import Alert from "/static/js/modules/classes/Alert.js";
import { goStep, toggleSkip } from "./stepper.js";

const stepDataKeys = {
    instalaciones: {
        annotation: "tipo",
        title: "ubicacion",
        icon: "ri-map-fill",
        saveHandler: (container) => () => AssociatedRecords.saveDBRecords("/eventos/api/asignar-instalaciones/", "instalaciones", container)
    },
    organizadores: {
        annotation: "rol",
        title: "nombreCompleto",
        icon: "ri-map-pin-user-fill",
        saveHandler: (container) => () => AssociatedRecords.saveDBRecords("/eventos/api/asignar-organizadores/", "organizadores", container)
    },
}

export default class AssociatedRecords{
    static addRecord(data, type, containerSelector, recordUI = null) {
        // Save the id/data in the corresponding array
        const isFormData = data instanceof FormData;
        
        // Extract id
        const id = isFormData ? data.get("id") : data["id"];
        const record = isFormData ? data : { id: data["id"] }
        const added = dataStore.addRecord(type, record, id);

        //If it already exists, return
        if (!added) {
            Alert.error(`El registro con id ${id} ya fue agregado`)
            return;
        }

        //* Append to the UI
        const container = document.querySelector(containerSelector);
        const dataUI = isFormData ? recordUI : data;
        this.addRecordToUI(id, dataUI, type, isFormData, container)
    }

    static addRecordToUI(id, data, type, isFormData, container){
        const step = container.closest('.main__step');
        const buttonStep = step.querySelector('.step__actions .step__button--next');

        const stepCard = document.createElement("DIV");
        stepCard.classList.add("step__card")
        stepCard.dataset.id = id;

        const cardContent = document.createElement("DIV");
        cardContent.classList.add("card__content");

        const cardHeader = document.createElement("DIV");
        cardHeader.classList.add("card__header")

        const cardAnnotation = document.createElement("SPAN");
        cardAnnotation.classList.add("card__annotation")
        cardAnnotation.textContent = data[stepDataKeys[type]["annotation"]];

        const cardTitle = document.createElement("H4");
        cardTitle.classList.add("card__title")
        cardTitle.textContent = data[stepDataKeys[type]["title"]];

        cardHeader.appendChild(cardAnnotation);
        cardHeader.appendChild(cardTitle);

        const cardButtons = document.createElement("DIV");
        cardButtons.classList.add("card__buttons");
        
        let cardButtonViewMore;
        if (type !== "instalaciones") {
            cardButtonViewMore = document.createElement("BUTTON");
            cardButtonViewMore.type = "button";
            cardButtonViewMore.classList.add("card__button")
            cardButtonViewMore.textContent = "Ver más detalle";
            cardButtonViewMore.onclick = () => alert("Mostrando más cositas", id)
        }

        //* Disassociate button
        const cardButtonDisassociate = document.createElement("BUTTON");
        cardButtonDisassociate.type = "button";
        cardButtonDisassociate.classList.add("card__button", "card__button--danger")
        cardButtonDisassociate.textContent = "Desvincular";
        cardButtonDisassociate.onclick = () => this.removeRecord(type, id, stepCard, buttonStep, container);

        if (cardButtonViewMore) cardButtons.appendChild(cardButtonViewMore);
        cardButtons.appendChild(cardButtonDisassociate);

        cardContent.appendChild(cardHeader);
        cardContent.appendChild(cardButtons)

        const cardIcon = document.createElement("DIV");
        cardIcon.classList.add("card__icon");
        cardIcon.innerHTML = `<i class="${stepDataKeys[type]["icon"]}"></i>`;

        stepCard.appendChild(cardContent);
        stepCard.appendChild(cardIcon)

        container.appendChild(stepCard)

        if (buttonStep.hasAttribute('data-skip')) toggleSkip(buttonStep, false, stepDataKeys[type].saveHandler(container))
    }

    static async removeRecord(type, id, stepCard, buttonStep, container){
        const result = await Alert.confirmationAlert({
            title: "Desvincular registro",
            text: "¿Está seguro que desea desvincular el registro seleccionado?",
            confirmButtonText: "Desvincular",
            cancelButtonText: "Cancelar"
        });
    
        if (!result.isConfirmed) return;
        dataStore.removeRecord(type, id);
        stepCard.remove();

        if (dataStore[type].length === 0) toggleSkip(buttonStep, true, stepDataKeys[type].saveHandler(container))
    }

    static async saveDBRecords(endpoint, type, container){
        const records = dataStore[type];

        if (!validateCollection(type, records)) {
            Alert.error(`Datos de ${type} inválidos`);
            return
        }

        const isFormData = records[0] instanceof FormData;

        let result;
        if (isFormData) {
            const bigForm = mergeFormDataArray(records, type);
            result = await API.postFormData(endpoint, bigForm);
        } else {
            result = await API.post(endpoint, JSON.stringify({ evento: dataStore.eventoId, records }));
        }

        if (result.error) {
            dataStore.excludeRecords(type, result.errores, container);
            return;    
        }

        Alert.success(`Datos de ${type} guardados correctamente.`);
        goStep("next")
    }
}