import { formDataToJSON, getCookie } from "../forms/utils.js";
import Alert from "./Alert.js";

export default class API {
    static async post(url, requestBody) {
        // Get csrf token
        const csrf = getCookie("csrftoken")

        // Detect whether the body is FormData or an object/JSON
        const isFormData = requestBody instanceof FormData;

        let jsonBody = requestBody; 
        
        //Convert the formData to JSON
        if (isFormData) jsonBody = formDataToJSON(jsonBody);

        try {
            // Fetch the endpoint
            const res = await fetch(url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrf,
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                body: jsonBody
            });

            const json = await res.json();

            if (!res.ok) {
                // Normalize error messages from backend (can be string or object of arrays)
                let msg = (json && json.error) || null;
                if (msg && typeof msg === 'object') {
                    try {
                        // Flatten values (strings or arrays) and join
                        const parts = Object.values(msg).flatMap(v => Array.isArray(v) ? v : [String(v)]);
                        msg = parts.join(' ');
                    } catch (_) {
                        msg = "¡Error en la operación!";
                    }
                }
                if (!msg || typeof msg !== 'string') {
                    msg = "¡Error en la operación!";
                }
                Alert.error(msg)
                return { error: true, data: json }
            }

            return { error: false, data: json };
        } catch (err) {
            // Network error or other type of exception
            Alert.error(err.message || `¡Error de Red!`)
            return { error: true };
        }
    }

    static async postFormData(url, formData) {
        const csrf = getCookie("csrftoken");
    
        try {
            const res = await fetch(url, {
                method: "POST",
                headers: { "X-CSRFToken": csrf },
                body: formData
            });
    
            const json = await res.json();
            if (!res.ok) {
                Alert.error(json.error || "¡Error en la operación!");
                return { error: true };
            }
            return { error: false, data: json };
        } catch (err) {
            Alert.error(err.message || "¡Error de Red!");
            return { error: true };
        }
    }    

    static async fetchGet(url) {
        try {
            // Fetch the endpoint
            const res = await fetch(url);
            const json = await res.json();

            if (!res.ok) {
                Alert.error(json.error ||`¡Error en la operación!`)
                return { error: true };
            }

            return { error: false, data: json };
        } catch (err) {
            // Network error or other type of exception
            Alert.error(err.message || `¡Error de Red!`)
            return { error: true };
        }
    }
}