const dataStore = {
    eventoId: getEventId(),
    instalaciones: [],
    organizadores: [],
    organizaciones: [],

    addRecord(type, record, id) {
        const alreadyExists = this[type].some(item => {
            const existingId = item instanceof FormData ? Number(item.get('id')) : item.id;
            return existingId == id;
        });
        if (alreadyExists) return false
        this[type].push(record);
        //! QUITAR METODO
        this.listFormDataRecords(type)
        return { success: true, message: "Registro agregado correctamente" };
    },

    getAllRecords(type){
        return this[type];
    },

    getByID(type, id) {
        return this[type].find(item => {
            if (item instanceof FormData) {
                return Number(item.get("id")) == Number(id);
            } else {
                return item.id == id;
            }
        }) || null;
    },   

    listFormDataRecords(type){
        dataStore[type].forEach((record, index) => {
            console.log(`Registro #${index}:`);
            if (record instanceof FormData) {
                for (let [key, value] of record.entries()) {
                    if (value instanceof File) {
                        console.log(`  ${key}: File { name: ${value.name}, size: ${value.size} }`);
                    } else {
                        console.log(`  ${key}: ${value}`);
                    }
                }
            } else {
                console.log("Record no es FormData:", record);
            }
        });
    },
    
    updateRecord(type, newRecord) {
        const id = newRecord instanceof FormData ? newRecord.get('id') : newRecord.id;
        let updated = false;
    
        this[type] = this[type].map(item => {
            const existingId = item instanceof FormData ? item.get('id') : item.id;
            if (existingId == id) {
                updated = true;
                return newRecord;
            }
            return item;
        });
    
        this.listFormDataRecords(type)
        if (!updated) return { success: false, message: "No se encontró el registro a actualizar" };
        return { success: true, message: "Registro actualizado correctamente" };
    },        

    removeRecord(type, id) {
        const initialLength = this[type].length;
    
        this[type] = this[type].filter(item => {
            if (item instanceof FormData) {
                return item.get('id') !== id;
            }
            return item.id !== id;
        });
    
        this.listFormDataRecords(type);
    
        if (this[type].length < initialLength) {
            return { success: true, message: "Registro eliminado correctamente" };
        } else {
            return { success: false, message: "No se encontró el registro a eliminar" };
        }
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

function getEventId() {
  const path = window.location.pathname;
  const parts = path.split('/').filter(Boolean);
  const lastSegment = parts[parts.length - 1];
  const isNumeric = /^\d+$/.test(lastSegment);
  return isNumeric ? parseInt(lastSegment, 10) : null;
}

export default dataStore;