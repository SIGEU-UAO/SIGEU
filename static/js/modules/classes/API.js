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
                Alert.error(json.error || `¡Error en la operación!`)
                return { error: true };
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
                Alert.error(json.error || `¡Error en la operación!`)
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