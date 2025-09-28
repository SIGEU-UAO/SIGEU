const validationSchemas = {
    instalaciones: {
        requiredKeys: ["id"], 
        types: { id: "number" } 
    }
};

// * Generic validation function
export function validateCollection(type, arr) {
    const schema = validationSchemas[type];
    if (!schema) throw new Error(`No hay esquema para el tipo: ${type}`);
    if (!Array.isArray(arr) || arr.length === 0) return false;

    return arr.every(obj => {
        if (typeof obj !== "object" || obj === null) return false;

        const keys = Object.keys(obj);
        // * It must have exactly the required keys.
        if (keys.length !== schema.requiredKeys.length) return false;
        if (!schema.requiredKeys.every(k => keys.includes(k))) return false;

        // * Each property must be of the correct type.
        return schema.requiredKeys.every(k => typeof obj[k] === schema.types[k]);
    });
}