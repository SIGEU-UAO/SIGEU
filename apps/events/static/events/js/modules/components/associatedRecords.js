import dataStore from "../dataStore.js";
import { validateCollection } from "../utils/validations.js";
import { mergeFormDataArray, handleFileInputsInfo } from "/static/js/modules/forms/utils.js";
import Modal from "/static/js/modules/classes/Modal.js";
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
        const result = dataStore.addRecord(type, record, id);

        //If it already exists, return
        if (!result) {
            Alert.error(`El registro con id ${id} ya fue agregado`)
            return;
        }

        Alert.success(result.message);

        //* Append to the UI
        const container = document.querySelector(containerSelector);
        const dataUI = isFormData ? recordUI : data;
        this.addRecordToUI(id, dataUI, type, isFormData, container)
    }

    static editRecord(record, type, containerSelector, form, isCurrentUser = false) {
        const id = record instanceof FormData ? record.get('id') : record.id;
        const container = document.querySelector(containerSelector);
        const buttonStep = container.nextElementSibling.lastElementChild;
    
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
        if (type !== "organizadores") this.updateRecordUI(type, record, container);
    
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
        
        const { success, message } = dataStore.removeRecord(type, id);

        if (success) {
            Alert.success(message);
            stepCard.remove();
        } else {
            Alert.error(message);
        }

        this.updateStepBtn(type, buttonStep, container)
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
        goStep("next")
    }

    //TODO: DECIDIR SI ELIMINAR PARAMETRO ISFORMDATA
    static addRecordToUI(id, data, type, isFormData, container, isCurrentUser = false){
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

    // TODO: ESTA FUNCION HAY QUE IMPLEMENTARLA CORRECTAMENTE PARA ORGANIZACIONES EXTERNAS
    static updateRecordUI(type, record, container){
        const id = record instanceof FormData ? record.get('id') : record.id;
        const card = container.querySelector(`.step__card[data-id="${id}"]`);
        if (!card) return;
    
        // Update visible fields
        const annotationKey = stepDataKeys[type].annotation;
        const titleKey = stepDataKeys[type].title;
    
        const annotation = record instanceof FormData ? record.get(annotationKey) : record[annotationKey];
        const title = record instanceof FormData ? record.get(titleKey) : record[titleKey];
    
        const cardAnnotation = card.querySelector('.card__annotation');
        const cardTitle = card.querySelector('.card__title');
    
        if (cardAnnotation) cardAnnotation.textContent = annotation;
        if (cardTitle) cardTitle.textContent = title;
    }    

    static updateStepBtn(type, buttonStep, container){
        const recordsLength = dataStore[type]?.length || 0;

        if (recordsLength > 0) {
            if (buttonStep.hasAttribute('data-skip')) {
                toggleSkip(buttonStep, false, stepDataKeys[type].saveHandler(container));
            }
        } else {
            toggleSkip(buttonStep, true, stepDataKeys[type].saveHandler(container));
        }
    }
}