import API from "./API.js";
import Alert from "./Alert.js";
import Loader from "./Loader.js"

const modalOpeners = [
    { buttonId: 'asignar-instalacion-btn', modalId: 'modal-instalaciones' }
];

export default class Modal{
    //* Initialize all modals and their steps/progress
    static initModals() {
        modalOpeners.forEach(({ buttonId, modalId }) => {
            const button = document.getElementById(buttonId);
            const modal = document.getElementById(modalId);
            if (!button || !modal) return;
    
            const radios = modal.querySelectorAll('input[name="steps"]');
            const steps = modal.querySelectorAll('.modal__step');
            const progressBar = modal.querySelector('.progress__bar');
            const totalSteps = radios.length;
    
            // Handles any search form in a generic way
            const updateSteps = () => {
                let activeIndex = 0;
                radios.forEach((radio, i) => {
                    if (radio.checked) activeIndex = i;
                });
    
                steps.forEach((step, i) => {
                    const active = i === activeIndex;
                    step.style.display = active ? 'flex' : 'none';
                    step.style.opacity = active ? '1' : '0';
                    step.style.transform = active ? 'translateY(0)' : 'translateY(20px)';
                });
    
                if (progressBar) {
                    progressBar.style.width = `${Math.round(((activeIndex + 1) / totalSteps) * 100)}%`;
                }
            };
    
            // Listen to radio changes
            radios.forEach(radio => radio.addEventListener('change', updateSteps));
    
            // Open modal and force initial step to be displayed
            button.addEventListener('click', () => {
                modal.show();
                updateSteps();
            });
    
            // Initialize modal close buttons
            this.initCloseButtons(modal);
        });
    }
    
    //* Init close modal buttons
    static initCloseButtons(modal) {
        modal.querySelectorAll('.modal__close').forEach(btn => 
            btn.addEventListener('click', () => Modal.closeModal(modal))
        );
    }

    static closeModal(modal){
        modal.close()
    }

    //* Toggle loader and results
    static toggleSearchState(loader, result) {
        Loader.toggleLoader(loader);
        result.classList.toggle("hide");
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
                    setTimeout(() => Modal.toggleSearchState(loader, result), 1500);
                    return;
                }

                const { items, message, messageType } = response.data;

                if (messageType === 'info') {
                    Alert.info(message);
                    setTimeout(() => {
                        Loader.toggleLoader(loader);
                        if (suggest) suggest.classList.remove('hide');
                    }, 1500);
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
    static displayCards(resultContainer, items, icon, fields, stepLabel = "Ver más", onClickCallback = () => {}) {
        // Limpiar contenedor
        resultContainer.innerHTML = '';

        items.forEach(item => {
            // Card principal
            const card = document.createElement("DIV");
            card.classList.add("entity__card");

            // Left div con icono e info
            const infoDiv = document.createElement("DIV");
            infoDiv.classList.add("entity__info");

            const iconDiv = document.createElement("DIV");
            iconDiv.classList.add("entity__icon");
            iconDiv.innerHTML = `<i class="${icon}"></i>`; // Podrías recibir icono como argumento si quieres

            const descriptionDiv = document.createElement("DIV");
            descriptionDiv.classList.add("entity__description");

            fields.forEach(f => {
                const fieldEl = document.createElement(f.tag || 'SPAN');
                fieldEl.textContent = `${f.label}: ${item[f.key]}`;
                if (f.key === "capacidad") fieldEl.textContent = `${f.label}: ${item[f.key]} personas`;
                descriptionDiv.appendChild(fieldEl);
            });

            infoDiv.appendChild(iconDiv);
            infoDiv.appendChild(descriptionDiv);

            // Right div botón
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
}