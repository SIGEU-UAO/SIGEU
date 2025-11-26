const dataStore = {
    eventoId: getEventId(),
    instalaciones: [],
    instalaciones_cambios: [],
    organizadores: [],
    organizadores_cambios: [],
    organizaciones: [],
    organizaciones_cambios: [],

    addRecord(type, record, id) {
        const alreadyExists = this[type].some(item => {
            const existingId = item instanceof FormData ? Number(item.get('id')) : item.id;
            return existingId == id;
        });
        if (alreadyExists) return false
        this[type].push(record);
        return { success: true, message: "Registro agregado correctamente" };
    },

    //* Method to edit an event
    registerChange(type, id, action, record = null){
        const changes = this[`${type}_cambios`];
        const original = this[type];
        const isFormData = record instanceof FormData;

        // Helpers
        const getChangeId = (c) => c instanceof FormData ? Number(c.get('id')) : Number(c.id);
        const getChangeAction = (c) => c instanceof FormData ? c.get('accion') : c.accion;
        const setAction = (c, a) => c instanceof FormData ? c.set('accion', a) : c.accion = a;

        // Check if there is already a change registered for this id
        let idx = changes.findIndex(c => getChangeId(c) === Number(id));
        let exists = idx !== -1;
        const originalHas = original.some(r => Number(r instanceof FormData ? r.get("id") : r.id) === Number(id));

        // Prepare change to record if it is formdata
        if (record && record instanceof FormData) record.set("accion", action)

        //* -------------------- ADD A NEW RECORD --------------------
        if (action === "agregar") {
            if (exists && getChangeAction(changes[idx]) === "eliminar") {
                if (isFormData && originalHas) {
                    // Existed in DB → update with new data
                    setAction(record, "actualizar");
                    changes[idx] = record;
                    return { success: true, message: `Registro ${id} marcado para actualización.` };
                }else{
                    // Simple case → undo deletion only
                    changes.splice(idx, 1);
                    return { success: true, message: `Se restauró el registro ${id}.` };
                }
            }

            if ((exists && getChangeAction(changes[idx]) === "agregar") || (originalHas)) {
                return { success: false, message: `El registro con id ${id} ya existe o ya fue agregado.` };
            }
    
            changes.push(isFormData ? record : { id: Number(id), accion: "agregar" });
            return { success: true, message: `Se registró la adición del registro con id ${id}.` };
        }

        //* -------------------- UPDATE (only FormData) --------------------
        if (action === "actualizar") {
            const isUpdatable =
                originalHas ||
                (exists && ["agregar", "actualizar"].includes(getChangeAction(changes[idx])));

            if (!isUpdatable) {
                return { success: false, message: `No se puede actualizar un registro inexistente.` };
            }

            if (exists) {
                const existing = changes[idx];
                for (let [key, value] of record.entries()) existing.set(key, value);
                setAction(existing, "actualizar");
            } else {
                setAction(record, "actualizar");
                changes.push(record);
            }

            return { success: true, message: `Registro ${id} actualizado correctamente.` };
        }        

        // -------------------- REMOVE --------------------
        if (action === "eliminar") {
            if (!originalHas) {
                if (exists) {
                    const ch = getChangeAction(changes[idx]);
                    if (ch === "agregar" || ch === "actualizar") {
                        // It was a local addition: undo it.
                        changes.splice(idx, 1);
                        return { success: true, message: `Se deshizo la adición del registro ${id}.` };
                    }
                }
                // There is nothing in the database or local changes to undo -> cannot be deleted
                return { success: false, message: `El registro con id ${id} no existe y no puede eliminarse.` };
            }

            if (exists && getChangeAction(changes[idx]) === "agregar") {
                changes.splice(idx, 1);
                return { success: true, message: `Se restauró el registro ${id}.` };
            }

            if (exists && getChangeAction(changes[idx]) === "actualizar" && isFormData) {
                changes.splice(idx, 1);
            }

            // recompute idx/exists after possible splices to avoid reading undefined
            const newIdx = changes.findIndex(c => getChangeId(c) === Number(id));
            const newExists = newIdx !== -1;

            // If it is already marked as ‘delete’ -> we do not allow it to be duplicated.
            if (newExists && getChangeAction(changes[newIdx]) === "eliminar") {
                return { success: false, message: `El registro con id ${id} ya fue marcado para eliminación.` };
            }

            changes.push(isFormData ? record : { id: Number(id), accion: "eliminar" });
            return { success: true, message: `Se registró la eliminación del registro con id ${id}.` };
        }
        
        return { success: false, message: `Acción no válida: ${action}` };
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