import API from "./API.js";
import Alert from "./Alert.js";
import Loader from "./Loader.js"
import dataStore from "/static/events/js/modules/dataStore.js";
import { validarFormData, handleFileInputsInfo } from "../forms/utils.js";
import { modalOpeners, modalsConfig } from "../components/modalsConfig.js";
import AssociatedRecords from "/static/events/js/modules/components/associatedRecords.js";

export default class Modal{
    //* Initialize all modals and their steps/progress
    static initModals() {
        modalOpeners.forEach(({ buttonId, modalId }) => {
            const btn   = document.getElementById(buttonId);
            const modal = document.getElementById(modalId);

            const update = () => Modal.changeStep(modal);

            btn.addEventListener('click', () => { modal.show(); update(); });
            modal.querySelectorAll('input[name="steps"]').forEach(r => r.addEventListener('change', update));
            modal.querySelectorAll('.modal__btn--prev').forEach(btn => btn.addEventListener('click', () => Modal.goStep(modal, "prev")));
            modal.querySelectorAll('.form__group .input-checkbox').forEach(input => input.addEventListener('change', Modal.toggleRelatedCheckboxField));
            Modal.initCloseButtons(modal);
        });
    }

    //* Display the current step and update the progress bar */
    static changeStep(modal) {
        const radios = [...modal.querySelectorAll('input[name="steps"]')];
        const steps  = [...modal.querySelectorAll('.modal__step')];
        const bar    = modal.querySelector('.progress__bar');
        
        if (radios.length && !radios.some(r => r.checked)) radios[0].checked = true
        
        const current = modal.querySelector('input[name="steps"]:checked');
        const idx = radios.indexOf(current);

        steps.forEach((s, i) => {
            const active = i === idx;
            s.style.display   = active ? 'flex' : 'none';
            s.style.opacity   = active ? '1'   : '0';
            s.style.transform = active ? 'translateY(0)' : 'translateY(20px)';
        });

        if (bar) bar.style.width = `${((idx + 1) / radios.length) * 100}%`;
    }

    static goStep(modal, direction) {
        const radios = [...modal.querySelectorAll('input[name="steps"]')];
        let idx = radios.findIndex(r => r.checked);
        if (idx < 0) idx = 0;

        const target = typeof direction === 'number' 
            ? (direction >= 0 ? direction : idx + direction)
            : (direction === 'prev' ? idx - 1 : idx + 1);

        const clampedTarget = Math.max(0, Math.min(target, radios.length - 1));
        if (!radios[clampedTarget]) return;

        radios[clampedTarget].checked = true;
        radios[clampedTarget].dispatchEvent(new Event('change', { bubbles: true }));
    }
    
    //* Init close modal buttons
    static initCloseButtons(modal) {
        modal.querySelectorAll('.modal__close').forEach(btn => 
            btn.addEventListener('click', () => Modal.closeModal(modal))
        );
    }

    static openEditModal(modalId, stepIndex = 3) {
        const modal = document.getElementById(modalId);
        modal.show();

        // Go to the third step
        Modal.goStep(modal, stepIndex)

        // Hide progress bar if it exists
        const progress = modal.querySelector('.progress');
        progress.style.display = 'none';

        // Hide prev buttons in all steps
        modal.querySelectorAll('.modal__btn--prev').forEach(btn => btn.style.display = 'none');

        // Change the text on the main button to “Update.”
        const footerBtn = modal.querySelector(`.modal__step[data-step="${stepIndex}"] .modal__btn--primary`);
        if (footerBtn) footerBtn.textContent = 'Actualizar';

        // Listener to close and reset the modal
        const closeBtns = modal.querySelectorAll('.modal__close');
        closeBtns.forEach(btn => {
            const handler = () => Modal.resetEditModal(modal, stepIndex);
            btn.addEventListener('click', handler, { once: true });
        });

        return modal;
    }

    static loadEditModalForm(record, form, type, callback, modalConfig, isCurrentUser = false){
        for (let [key, value] of record.entries()) {
            const input = form.querySelector(`[name="${key}"]`);
            if (!input) continue;

            if (input.type === "file") {
                // Display file name in file info
                const fileObj = record instanceof FormData ? record.get(key) : null;
                input.removeAttribute("required");
                handleFileInputsInfo(input, fileObj);
            } else if (input.type === "checkbox" || input.type === "radio") {
                input.checked = input.value == value;
                input.dispatchEvent(new Event('change', { bubbles: true }));
            } else {
                input.value = value;
            }
        }

        form.onsubmit = (e) => callback(e, record, type, form, modalConfig, isCurrentUser);
    }

    static closeModal(modal){
        modal.close()
    }

    static resetModal(modal, associationForm){
        // Reset form association
        associationForm.reset();
        associationForm.removeAttribute("data-id");
        associationForm.querySelectorAll('.file-info').forEach(div => div.textContent = '');

        // Rehabilitate all related fields
        Modal.enableRelatedFields(associationForm);

        // Reset record details
        const list = modal.querySelector('.modal__list');
        list.innerHTML = '';

        Modal.goStep(modal, 0) // Go to the first modal step
        Modal.closeModal(modal)
    }

    static resetEditModal(modal, currentStep = 3) {
        setTimeout(() => {
            // Go to first step
            Modal.goStep(modal, 0)

            // Restore progress bar
            const progress = modal.querySelector('.progress');
            progress.style.display = '';

            // Restore prev buttons
            modal.querySelectorAll('.modal__btn--prev').forEach(btn => btn.style.display = '');

            // Restore main button text
            const footerBtn = modal.querySelector(`.modal__step[data-step="${currentStep}"] .modal__btn--primary`);
            if (footerBtn) footerBtn.textContent = 'Guardar';

            // Clear the associate form
            const form = modal.querySelector(`.modal__step[data-step="${currentStep}"] .modal__form`);
            form.onsubmit = null;
            if (form) form.reset();
            form.querySelectorAll('input[type="file"]').forEach(input => input.setAttribute('required', ''));
            form.querySelectorAll('.file-info').forEach(div => div.textContent = '');
            Modal.enableRelatedFields(form);

            modal.close();
        }, 500);
    }

    //* Toggle loader and results
    static toggleSearchState(loader, result) {
        Loader.toggleLoader(loader);
        result.classList.toggle("hide");
    }

    //* Toggle related checkbox field
    static toggleRelatedCheckboxField(e){
        const checkbox = e.target;
        const relatedField = document.querySelector(`#${checkbox.dataset.related}`)
        
        if (checkbox.checked) {
            relatedField.setAttribute("disabled", "true")
            relatedField.classList.add("form__input--disabled")
            relatedField.value = "";
        }else{
            relatedField.removeAttribute("disabled")
            relatedField.classList.remove("form__input--disabled")
        }
    }

    static enableRelatedFields(form){
        form.querySelectorAll('[data-related]').forEach(cb => {
            const relatedField = document.getElementById(cb.dataset.related);
            if (relatedField) {
                relatedField.disabled = false;
                relatedField.classList.remove('form__input--disabled');
            }
        });
    }

     //* Handles any search form in a generic way
     static handleSearchFormSubmit({ formSelector, loaderSelector, resultSelector, suggestSelector, endpoint, valueField, displayCallback }) {
        const form = document.querySelector(formSelector);
        const loader = document.querySelector(loaderSelector);
        const result = document.querySelector(resultSelector);
        const suggest = suggestSelector ? document.querySelector(suggestSelector) : null;

        if (!form || !loader || !result) return;

        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            const searchInputValue = form[valueField]?.value.trim() || '';
            if (!searchInputValue) {
                Alert.error('El campo de búsqueda es obligatorio');
                return;
            }

            result.classList.add('hide');
            if (suggest) suggest.classList.add('hide');
            Loader.toggleLoader(loader);

            try {
                const response = await API.fetchGet(`${endpoint}?q=${encodeURIComponent(searchInputValue)}`);
                if (response.error) {
                    setTimeout(() => {
                        Modal.toggleSearchState(loader, result)
                    }, 1000);
                    return;
                }

                const { items, message, messageType } = response.data;

                if (messageType === 'info') {
                    Alert.info(message);
                    setTimeout(() => {
                        Loader.toggleLoader(loader);
                        if (suggest) suggest.classList.remove('hide');
                    }, 1000);
                    return;
                }

                if (displayCallback) displayCallback(result, items);
                Alert.success(message);
                Modal.toggleSearchState(loader, result);
            } catch (err) {
                console.log(err)
                Alert.error('Error al realizar la búsqueda');
                Loader.toggleLoader(loader);
            }
        });
    }

    //* Display cards generically in a modal
    static displayCards(resultContainer, items, icon, fields, stepLabel, onClickCallback = () => {}) {
        // Clean container
        resultContainer.innerHTML = '';

        items.forEach(item => {
            // Main card
            const card = document.createElement("DIV");
            card.classList.add("entity__card");

            // Left div with icon and info
            const infoDiv = document.createElement("DIV");
            infoDiv.classList.add("entity__info");

            const iconDiv = document.createElement("DIV");
            iconDiv.classList.add("entity__icon");
            iconDiv.innerHTML = `<i class="${icon}"></i>`;

            const descriptionDiv = document.createElement("DIV");
            descriptionDiv.classList.add("entity__description");

            fields.forEach(f => {
                const fieldEl = document.createElement(f.tag || 'SPAN');
                fieldEl.textContent = f.label === "" ? `${item[f.key]}` : `${f.label}: ${item[f.key]}`;
                if (f.key === "capacidad") fieldEl.textContent = `${f.label}: ${item[f.key]} personas`;
                descriptionDiv.appendChild(fieldEl);
            });

            infoDiv.appendChild(iconDiv);
            infoDiv.appendChild(descriptionDiv);

            // Right div button
            const btn = document.createElement("BUTTON");
            btn.type = "button";
            btn.classList.add("entity__btn");
            btn.innerHTML = `<label for='${stepLabel.toLowerCase().replace(/\s+/g,'-')}'>${stepLabel}</label>`;
            btn.addEventListener('click', () => onClickCallback(resultContainer, item));

            // Append a card
            card.appendChild(infoDiv);
            card.appendChild(btn);

            resultContainer.appendChild(card);
        });
    }

    //* View more details
    static renderDetailStep(modal, item, type){
        const list = modal.querySelector('.modal__list');

        // Clear any previous content
        list.innerHTML = '';

        // We go through the properties of the object
        Object.entries(item).forEach(([key, value]) => {
            // Skip those beginning with “id”
            if (key.toLowerCase().startsWith('id')) return;

            // Create the <li>
            const li = document.createElement('li');
            li.classList.add('modal__li');

            const label = key
                .replace(/([A-Z])/g, ' $1')   // Separate camelCase
                .replace(/^./, c => c.toUpperCase()) + ':'; // Initial capital letter

            li.innerHTML = `<strong>${label}</strong> <span>${value ?? ''}</span>`;
            list.appendChild(li);
        });

        //* Add Event Listener to associate button
        const stepDetailButton = modal.querySelector(".modal__step[data-step='2'] .modal__btn--primary");
        const associateForm = modal.querySelector(".modal__step[data-step='3'] .modal__form");
        const idKey = Object.keys(item).find(k => k.toLowerCase().startsWith("id"));
        const id = item[idKey];

        stepDetailButton.addEventListener("click", () => {
            associateForm.dataset.id = id;
            Modal.goStep(modal, "next")
        })

        associateForm.onsubmit = (e) => Modal.handleAssociateForm(e, id, item, type);
    }

    //* New Associate Record
    static handleAssociateForm(e, itemID, item, type){
        e.preventDefault();

        const form = e.currentTarget;
        const formData = new FormData(form);
        formData.delete("csrfmiddlewaretoken"); // Delete the CSRF token
        const modalConfig = modalsConfig.find(config => config.type === type);

        // Add the id field
        formData.append('id', itemID);

        // Validate FormData
        if (!validarFormData(formData, modalConfig.associateValidationRules)) return;

        // Add record        
        const recordUI = {};
        if (modalConfig.fieldsRecordUI) modalConfig.fieldsRecordUI.forEach(field => recordUI[field] = item[field]);
        if (item.nombres && item.apellidos) recordUI.nombreCompleto = `${item.nombres} ${item.apellidos}`;

        const containerSelector = modalConfig.assignedRecordsContainerSelector;
        AssociatedRecords.addRecord(formData, type, containerSelector, recordUI);

        //Reset the modal
        const modal = document.getElementById(modalConfig.modalId);
        Modal.resetModal(modal, form)
    }

    //* Request to edit record
    static editRecordHandler(type, id) {
        const modalConfig = modalsConfig.find(config => config.type === type && config.editable);
        const modal = Modal.openEditModal(modalConfig.modalId);
        const form = modal.querySelector(modalConfig.associateFormSelector);
    
        let record = dataStore.getByID(type, id);
        const isCurrentUser = window.currentUser && window.currentUser.id == id;
    
        if (!record && isCurrentUser) {
            record = new FormData();
            record.append('id', id);
        }
    
        if (!record) {
            Alert.error("No se encontró el registro para editar");
            Modal.resetEditModal(modal);
            return;
        }
    
        // Load the form and assign the submit function
        Modal.loadEditModalForm(record, form, modalConfig.type, Modal.prepareFormDataForEdit, modalConfig, isCurrentUser);
    }    

    static prepareFormDataForEdit(e, record, type, form, modalConfig, isCurrentUser = false) {
        e.preventDefault();
    
        // Clone original record
        const updatedRecord = new FormData();
        for (let [key, value] of record.entries()) {
            updatedRecord.append(key, value);
        }
    
        // Overwrite with form fields
        new FormData(form).forEach((value, key) => {
            if (key === "csrfmiddlewaretoken") return; // Ignore the CSRF token
            if (form.querySelector(`[name="${key}"]`)?.type === "file" && !value.name) return;
            updatedRecord.set(key, value);
        });

        // For external organizations...
        if (type === "organizaciones") {
            const checkbox = form.querySelector('[name="representante_asiste"]');
            updatedRecord.delete(checkbox.checked ? "representante_alterno" : "representante_asiste")
        }

        const modal = document.getElementById(modalConfig.modalId);
        
        // Call the method that updates dataStore and UI
        AssociatedRecords.editRecord(updatedRecord, type, form, modal, modalConfig, isCurrentUser);
        
        //Reset the modal
        Modal.resetModal(modal, form)
    }    
}