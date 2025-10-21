import dataStore from "../dataStore.js";
import { validateCollection } from "../utils/validations.js";
import { validarFormData, mergeFormDataFieldsArray, mergeFormDataIndexed, handleFileInputsInfo } from "/static/js/modules/forms/utils.js";
import Modal from "/static/js/modules/classes/Modal.js";
import API from "/static/js/modules/classes/API.js";
import Alert from "/static/js/modules/classes/Alert.js";
import { finishStepHandler, goStep, toggleSkip } from "./stepper.js";

const mainForm = document.getElementById("main-form");
const mainFormAction = mainForm.getAttribute("data-action");

const stepDataKeys = {
    instalaciones: {
        annotation: "tipo",
        title: "ubicacion",
        icon: "ri-map-fill",
        saveHandler: (container) => () => {
            if (mainFormAction === "add") {
                AssociatedRecords.saveDBRecords("/eventos/api/asignar-instalaciones/", "instalaciones", container);
            } else if (mainFormAction === "edit") {
                AssociatedRecords.updateDBRecords("/eventos/api/actualizar-instalaciones/", "instalaciones", container);
            }
        }
    },
    organizadores: {
        annotation: "rol",
        title: "nombreCompleto",
        icon: "ri-map-pin-user-fill",
        saveHandler: (container) => () => AssociatedRecords.saveDBRecords("/eventos/api/asignar-organizadores/", "organizadores", container)
    },
    organizaciones: {
        annotation: "nit",
        title: "nombre",
        icon: "ri-building-2-fill",
        saveHandler: (container) => () => AssociatedRecords.saveDBRecords("/eventos/api/asignar-organizaciones/", "organizaciones", container, true, "/eventos/mis-eventos/")
    },
}

export default class AssociatedRecords{
    static addRecord(data, type, containerSelector, recordUI = null) {
        // Save the id/data in the corresponding array
        const isFormData = data instanceof FormData;
        
        // Extract id
        const id = isFormData ? data.get("id") : data["id"];
        const record = isFormData ? data : { id: data["id"] }

        let result;

        if (mainFormAction === "add"){
            result = dataStore.addRecord(type, record, id);

            //If it already exists, return
            if (!result) {
                Alert.error(`El registro con id ${id} ya fue agregado`)
                return;
            }
        }
        else if (mainFormAction === "edit"){
            result = dataStore.registerChange(type, id, 'agregar');

            if (!result.success) {
                Alert.error(result.message);
                return;
            }
        }

        Alert.success(result.message);

        //* Append to the UI
        const container = document.querySelector(containerSelector);
        const dataUI = isFormData ? recordUI : data;
        if (isFormData && type === "organizaciones") {
            recordUI["associate_fields"] = [data.get("representante_asiste") === "on" ? "El representante legal ASISTE" : "El representante legal NO ASISTE"]
            if (data.get("representante_alterno")) recordUI["associate_fields"].push(`Representante alterno: ${data.get("representante_alterno")}`)
        }

        this.addRecordToUI(id, dataUI, type, container)
    }

    static editRecord(record, type, form, modal, modalConfig, isCurrentUser = false) {
        const id = record instanceof FormData ? record.get('id') : record.id;
        const container = document.querySelector(modalConfig.assignedRecordsContainerSelector);
        const buttonStep = container.nextElementSibling.lastElementChild;

        // Validate formData
        if (!validarFormData(record, modalConfig.associateValidationRules)) {
            Modal.resetEditModal(modal);
            return;
        };
    
        // Update or add as appropriate and capture the result
        let result;
        if (!dataStore.getByID(type, id) && isCurrentUser) {
            result = dataStore.addRecord(type, record, id);
            this.updateStepBtn(type, buttonStep, container);
        } else {
            result = dataStore.updateRecord(type, record);
        }
    
        // Display message to user based on result
        if (result) {
            if (result.success) {
                Alert.success(result.message);
            } else {
                Alert.error(result.message);
                return;
            }
        }
    
        // Update the UI
        if (type !== "organizadores") this.updateRecordUI(record, container);
    
        // Update file input info
        form.querySelectorAll('input[type="file"]').forEach(input => {
            const existingFile = record.get(input.name);
            handleFileInputsInfo(input, existingFile);
        });
    }    

    static async removeRecord(type, id, stepCard, buttonStep, container){
        const result = await Alert.confirmationAlert({
            title: "Desvincular registro",
            text: "¿Está seguro que desea desvincular el registro seleccionado?",
            confirmButtonText: "Desvincular",
            cancelButtonText: "Cancelar"
        });
    
        if (!result.isConfirmed) return;

        let success = false;
        let message = "";

        if (mainFormAction === "add") {
            const removeResult = dataStore.removeRecord(type, id);
            success = removeResult.success;
            message = removeResult.message;
        } 
        else if (mainFormAction === "edit") {
            const registerResult = dataStore.registerChange(type, id, "eliminar");
            success = registerResult.success;
            message = registerResult.message;
        }

        if (success) {
            Alert.success(message);
            stepCard.remove();
            this.updateStepBtn(type, buttonStep, container);
        } else {
            Alert.error(message);
        }
    }

    static async saveDBRecords(endpoint, type, container, isFinishStep = false, finishURL = ""){
        const records = dataStore[type];

        if (!validateCollection(type, records)) {
            Alert.error(`Datos de ${type} inválidos`);
            return
        }

        const isFormData = records[0] instanceof FormData;

        let result;
        if (isFormData) {
            const bigForm = (type === "organizaciones")
                ? mergeFormDataIndexed(records, type)
                : mergeFormDataFieldsArray(records, type);
            bigForm.append("evento", dataStore.eventoId);
            result = await API.postFormData(endpoint, bigForm);
        } else {
            result = await API.post(endpoint, JSON.stringify({ evento: dataStore.eventoId, records }));
        }

        if (result.error) {
            if (result.data.errores) dataStore.excludeRecords(type, result.data.errores, container);
            return;    
        }

        Alert.success(`Datos de ${type} guardados correctamente.`);
        
        if (isFinishStep) {
            setTimeout(() => window.location.href = finishURL, 1500);
        }else{
            goStep("next")
        }
    }

    static async updateDBRecords(endpoint, type, container, isFinishStep = false, finishURL = ""){
        const eventoId = dataStore.eventoId;
        const updatedRecords = dataStore[`${type}_cambios`] || [];
        const originalRecords = dataStore[type] || [];

        const originalIds = originalRecords.map(r => typeof r === "object" ? r.id : r);
        let finalIds = [...originalIds];

        // Apply the changes
        for (const { id, accion } of updatedRecords) {
            if (accion === "agregar" && !finalIds.includes(id)) finalIds.push(id);
            if (accion === "eliminar") finalIds = finalIds.filter(x => x !== id);
        }

        const noChanges = originalIds.length === finalIds.length && originalIds.every(id => finalIds.includes(id)); 
        if (noChanges) {
            goStep("next");
            return;
        }

        const body = JSON.stringify({ records: updatedRecords});
        const result = await API.put(`${endpoint}${eventoId}/`, body);
        if (result.error) {
            if (result.data.errores) dataStore.excludeRecords(type, result.data.errores, container);
            return;
        };

        // Update the base dataStore with the new records and clean up the changes.
        dataStore[type] = finalIds.map(id => ({ id: Number(id) }));
        dataStore[`${type}_cambios`] = [];
        Alert.success(`Datos de ${type} actualizados correctamente.`);

        if (isFinishStep) {
            setTimeout(() => window.location.href = finishURL, 1500);
        } else {
            goStep("next");
        }
    }

    static addRecordToUI(id, data, type, container, isCurrentUser = false){
        const buttonStep = container.nextElementSibling.lastElementChild;

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

        if (type === "organizaciones") {
            const cardList = document.createElement("UL");
            cardList.classList.add("card__list")

            data["associate_fields"].forEach((field, index) => {
                const cardListItem = document.createElement("LI");
                cardListItem.textContent = field;
                cardListItem.classList.add('card__item')
                cardList.appendChild(cardListItem)
            })

            cardHeader.appendChild(cardList)
        }

        const cardButtons = document.createElement("DIV");
        cardButtons.classList.add("card__buttons");
        
        let cardButtonEdit;
        if (type !== "instalaciones") {
            cardButtonEdit = document.createElement("BUTTON");
            cardButtonEdit.type = "button";
            cardButtonEdit.classList.add("card__button")
            cardButtonEdit.textContent = "Editar";
            cardButtonEdit.onclick = () => Modal.editRecordHandler(type, id)
        }

        //* Disassociate button
        let cardButtonDisassociate;
        if (!isCurrentUser) {
            cardButtonDisassociate = document.createElement("BUTTON");
            cardButtonDisassociate.type = "button";
            cardButtonDisassociate.classList.add("card__button", "card__button--danger")
            cardButtonDisassociate.textContent = "Desvincular";
            cardButtonDisassociate.onclick = () => this.removeRecord(type, id, stepCard, buttonStep, container);   
        }

        if (cardButtonEdit) cardButtons.appendChild(cardButtonEdit);
        if (cardButtonDisassociate) cardButtons.appendChild(cardButtonDisassociate);

        cardContent.appendChild(cardHeader);
        cardContent.appendChild(cardButtons)

        const cardIcon = document.createElement("DIV");
        cardIcon.classList.add("card__icon");
        cardIcon.innerHTML = `<i class="${stepDataKeys[type]["icon"]}"></i>`;

        stepCard.appendChild(cardContent);
        stepCard.appendChild(cardIcon)

        container.appendChild(stepCard)

        this.updateStepBtn(type, buttonStep, container)
    }

    // * Function to update the record in UI (Applies only to external organizations...)
    static updateRecordUI(record, container){
        const id = record.get('id');
        const card = container.querySelector(`.step__card[data-id="${id}"]`);
        if (!card) return;
    
        // Update visible fields
        const cardList = card.querySelector(".card__list")
        let cardListItems = card.querySelectorAll(".card__item");

        if (record.has("representante_asiste") || record.has("representante_alterno")) {
            const representanteAsiste = record.get("representante_asiste");
            const representanteAlterno = record.get("representante_alterno");

            const texts = [representanteAsiste === "on" ? "El representante legal ASISTE" : "El representante legal NO ASISTE"];
            if (representanteAlterno) texts.push(`Representante alterno: ${representanteAlterno}`)

            while (cardListItems.length < texts.length) {
                const newItem = document.createElement("li");
                newItem.classList.add("card__item");
                cardList.appendChild(newItem);
                cardListItems = card.querySelectorAll(".card__item");
            }

            while (cardListItems.length > texts.length) {
                cardListItems[cardListItems.length - 1].remove();
                cardListItems = cardList.querySelectorAll(".card__item");
            }

            // Replace the content of visible items
            cardListItems.forEach((item, index) => {
                item.textContent = texts[index] || "";
            });
        }
    }    

    static updateStepBtn(type, buttonStep, container){
        const recordsLength = dataStore[type]?.length || 0;
        const isEnabledToSkip = recordsLength === 0 && dataStore[`${type}_cambios`].length === 0;

        if (buttonStep.classList.contains("step__button--finish")) {
            finishStepHandler(buttonStep, recordsLength, stepDataKeys[type].saveHandler(container), "/eventos/mis-eventos/");
        } else {
            toggleSkip(buttonStep, isEnabledToSkip, stepDataKeys[type].saveHandler(container));
        }
    }
}