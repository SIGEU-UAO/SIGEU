const validationSchemas = {
    instalaciones: {
        requiredKeys: ["id"], 
        types: { id: "number" } 
    },
    organizadores: {
        requiredKeys: ["id", "aval"], 
        types: { id: "string", aval: "file" }
    }
};

// * Generic validation function
export function validateCollection(type, arr) {
    const schema = validationSchemas[type];
    if (!schema) throw new Error(`No hay esquema para el tipo: ${type}`);
    if (!Array.isArray(arr) || arr.length === 0) return false;
    
    return arr.every(item => {
        let getValue, keys;

        if (item instanceof FormData) {
            keys = Array.from(item.keys());
            getValue = k => item.get(k);
        } else if (typeof item === "object" && item !== null) {
            keys = Object.keys(item);
            getValue = k => item[k];
        } else {
            return false;
        }

        // * Validate keys
        if (keys.length !== schema.requiredKeys.length) return false;
        if (!schema.requiredKeys.every(k => keys.includes(k))) return false;

        // * Validate types
        return schema.requiredKeys.every(k => {
            const expectedType = schema.types[k];
            const value = getValue(k);

            if (expectedType === "file") {
                if (!(value instanceof File)) return false;
                const isPDFType = value.type === "application/pdf";
                const isPDFExtension = value.name?.toLowerCase().endsWith(".pdf");
                return isPDFType || isPDFExtension;
            }

            return typeof value === expectedType;
        });
    });
}