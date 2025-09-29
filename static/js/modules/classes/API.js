import { formDataToJSON, getCookie } from "../forms/utils.js";
import Alert from "./Alert.js";

export default class API {
    /**
     * Realiza una petición POST a la URL dada con el formData o JSON proporcionado.
     * Retorna un objeto { error, data }.
     */
    static async post(url, formData) {
        // Get csrf token
        const csrf = getCookie("csrftoken")

        //Convert the formData to JSON
        const jsonBody = formDataToJSON(formData);

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
                // Do not alert here to avoid duplicate toasts; let caller decide how to show errors
                return { error: true, data: json };
            }

            return { error: false, data: json };
        } catch (err) {
            // Network error or other type of exception
            Alert.error(err.message || `¡Error de Red!`)
            return { error: true };
        }
    }

    static async fetchGet(url) {
        try {
            // Fetch the endpoint
            const res = await fetch(url);
            const json = await res.json();

            if (!res.ok) {
                Alert.error(`¡Error en la operación!`);
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