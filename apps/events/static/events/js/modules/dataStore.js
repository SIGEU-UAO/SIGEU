const dataStore = {
    eventoId: null,
    instalaciones: [],
    organizadores: [],
    organizaciones: [],

    addRecord(type, record) {
        const alreadyExists = this[type].some(item => item.id === record.id);
        if (alreadyExists) return false
        this[type].push(record);
        return true;
    },

    removeRecord(type, id) {
        this[type] = this[type].filter(item => item.id !== id);
    },

    clear(type) {
        this[type] = [];
    }
};

export default dataStore;