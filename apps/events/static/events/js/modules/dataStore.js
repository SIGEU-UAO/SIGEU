const dataStore = {
    eventoId: null,
    instalaciones: [],
    organizadores: [],
    organizaciones: [],

    addRecord(type, record, id) {
        // TODO: REVISAR ALREADY EXSITS PARA FORMDATA
        const alreadyExists = this[type].some(item => item.id === id);
        if (alreadyExists) return false
        this[type].push(record);
        return true;
    },

    removeRecord(type, id) {
        this[type] = this[type].filter(item => item.id !== id);
    },

    getAllRecords(type){
        return this[type];
    },

    excludeRecords(type, idsArray, container) {
        if (!Array.isArray(this[type])) return;
    
        // Exclude from data
        const ids = idsArray.map(obj => obj.id);
        this[type] = this[type].filter(item => !ids.includes(item.id));
    
        // Reset the UI
        idsArray.forEach(id => {
            const card = container.querySelector(`.step__card[data-id="${id}"]`);
            if (card) card.remove();
        });

        // Check if there are no more records and adjust button
        const step = container.closest('.main__step');
        const buttonStep = step?.querySelector('.step__actions .step__button--next');
        if (buttonStep && this[type].length === 0) {
            buttonStep.setAttribute('data-skip', '');
            buttonStep.textContent = 'Omitir';
        }
    },    

    clear(type) {
        this[type] = [];
    }
};

export default dataStore;