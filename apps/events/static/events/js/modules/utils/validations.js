const validationSchemas = {
    instalaciones: {
        requiredKeys: ["id"], 
        types: { id: "number" } 
    },
    organizadores: {
        requiredKeys: ["id", "aval"], 
        types: { id: "string", aval: "file" }
    },
    organizaciones: {
        requiredKeys: ["id", "certificado_participacion"], 
        optionalExclusiveKeys: ["representante_asiste", "representante_alterno"],
        types: {
            id: "string", 
            certificado_participacion: "file"
        }
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
        if (!schema.requiredKeys.every(k => keys.includes(k))) return false;

        // * Validate required fields types
        const requiredValid = schema.requiredKeys.every(k => {
            const expectedType = schema.types[k];
            const value = getValue(k);

            if (expectedType === "file") {
                if (!(value instanceof File)) return false;
                const isPDFType = value.type === "application/pdf";
                const isPDFExtension = value.name?.toLowerCase().endsWith(".pdf");
                return isPDFType || isPDFExtension;
            }

            if (expectedType === "number")
                return !isNaN(Number(value)) && Number(value) > 0;

            return typeof value === expectedType;
        });

        if (!requiredValid) return false;

        // * Validate exclusive optional fields (if applicable)
        if (schema.optionalExclusiveKeys) {
            const presentOptionals = schema.optionalExclusiveKeys.filter(k => {
                const val = getValue(k);
                if (val === undefined || val === null) return false;
                if (k === "representante_asiste") return val === "on";
                return val.toString().trim() !== "";
            });

            // There must be 0 or 1 optional present (NOT more than one).
            if (presentOptionals.length > 1) return false;
        }

        const allowedKeys = [
            ...schema.requiredKeys,
            ...(schema.optionalExclusiveKeys || [])
        ];
        const invalidKeys = keys.filter(k => !allowedKeys.includes(k));
        if (invalidKeys.length > 0) return false;

        return true;
    });
}