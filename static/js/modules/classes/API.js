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
                let msg = json.error || "¡Error en la operación!";
                Alert.error(msg);
                return { error: true, data: json };
            }

            if (res.status === 207) {
                let msg = json.error || "Hubo errores parciales";
    
                if (json.errores && Array.isArray(json.errores) && json.errores.length > 0) {
                    const detalles = json.errores
                        .map(e => {
                            if (typeof e === "string") return e;
                            if (e && e.error) return `ID ${e.id || "?"}: ${e.error}`;
                            return JSON.stringify(e);
                        })
                        .join(" | ");
                    msg = `${msg} - ${detalles}`;
                }
    
                Alert.warning(msg);
                return { error: true, data: json };
            }

            return { error: false, data: json };
        } catch (err) {
            // Network error or other type of exception
            Alert.error(err.message || `¡Error de Red!`)
            return { error: true };
        }
    }

    static async put(url, requestBody) {
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
                method: "PUT",
                headers: {
                    "X-CSRFToken": csrf,
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                body: jsonBody
            });
            const json = await res.json();
            if (!res.ok) {
                let msg = json.error || "¡Error en la operación!";
                Alert.error(msg);
                return { error: true, data: json };
            }
            if (res.status === 207) {
                let msg = json.error || "Hubo errores parciales";
                if (json.errores && Array.isArray(json.errores) && json.errores.length > 0) {
                    const detalles = json.errores.map(e => {
                            if (typeof e === "string") return e;
                            if (e && e.error) return `ID ${e.id || "?"}: ${e.error}`;
                            return JSON.stringify(e);
                        }).join(" | ");
                    msg = `${msg} - ${detalles}`;
                }
                Alert.warning(msg);
                return { error: true, data: json };
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
                let msg = json.error || "¡Error en la operación!";
                Alert.error(msg);
                return { error: true, data: json };
            }

            if (res.status === 207) {
                let msg = json.error || "Hubo errores parciales";
    
                if (json.errores && Array.isArray(json.errores) && json.errores.length > 0) {
                    const detalles = json.errores
                        .map(e => {
                            if (typeof e === "string") return e;
                            if (e && e.error) return `ID ${e.id || "?"}: ${e.error}`;
                            return JSON.stringify(e);
                        })
                        .join(" | ");
                    msg = `${msg} - ${detalles}`;
                }
    
                Alert.warning(msg);
                return { error: true, data: json };
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

    static async delete(url, AlertTitle, AlertText, successText, errorText, datatableId) {
        const result = await Alert.confirmationAlert({
            title: AlertTitle,
            text: AlertText,
            confirmButtonText: "Eliminar",
            cancelButtonText: "Cancelar"
        });

        if (!result.isConfirmed) return;

        try {
            const response = await fetch(url, {
                method: "DELETE",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                },
                credentials: "same-origin"
            });

            if (response.ok || response.status === 404) {
                Alert.success(successText);

                if (datatableId) {
                    setTimeout(() => {
                        $(`#${datatableId}`).DataTable().ajax.reload(null, false);
                    }, 1500);
                }
            } else {
                const data = await response.json().catch(() => ({}));
                Alert.error(data.error || errorText);
            }

        } catch (err) {
            Alert.error("Error de red. Intenta de nuevo.");
        }
    }
}