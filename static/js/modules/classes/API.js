import { formDataToJSON, getCookie } from "../forms/utils.js";
import Alert from "./Alert.js";
import { loginUrl } from "/static/js/base.js";

// Intenta parsear JSON de forma segura y detecta sesión expirada
async function parseJSONSafe(res) {
    try {
        const json = await res.json();
        return { ok: true, json };
    } catch (err) {
        const contentType = (res.headers.get("content-type") || "").toLowerCase();
        const url = res.url || "";

        // Caso típico: la sesión expiró, Django devolvió la página de login (HTML)
        if (contentType.includes("text/html") && url.includes("/users/inicio-sesion")) {
            Alert.error("Sesión expirada. Serás redirigido a la página de inicio de sesión.");
            setTimeout(() => {
                window.location.href = loginUrl;   // "/users/inicio-sesion/"
            }, 2000);
            return { ok: false, sessionExpired: true };
        }

        console.error("Error al parsear JSON de la respuesta:", err);
        Alert.error("Respuesta inesperada del servidor. Intenta nuevamente en unos momentos.");
        return { ok: false, sessionExpired: false };
    }
}

// Manejo centralizado de errores de red (cuando fetch revienta)
function handleNetworkError(err) {
    const raw = err && err.message ? String(err.message) : "";
    const lower = raw.toLowerCase();

    if (lower.includes("failed to fetch") || lower.includes("networkerror")) {
        Alert.error("No se pudo conectar con el servidor. Verifica tu conexión a Internet e inténtalo de nuevo.");
    } else {
        Alert.error("Ocurrió un error al comunicarse con el servidor. Intenta nuevamente en unos momentos.");
    }
}

export default class API {
    static async post(url, requestBody) {
        const csrf = getCookie("csrftoken");

        const isFormData = requestBody instanceof FormData;
        let jsonBody = requestBody;
        if (isFormData) jsonBody = formDataToJSON(jsonBody);

        try {
            const res = await fetch(url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrf,
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                body: jsonBody
            });

            const { ok, json, sessionExpired } = await parseJSONSafe(res);
            if (!ok) {
                // Si la sesión expiró o hubo respuesta no válida, ya mostramos mensaje
                if (sessionExpired) return { error: true };
                return { error: true };
            }

            if (!res.ok) {
                let msg = json.error || "¡Error en la operación!";

                if (res.status >= 500) {
                    msg = "Ocurrió un error interno en el servidor al guardar la información. Tus datos no se han perdido, por favor inténtalo nuevamente.";
                }

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
            handleNetworkError(err);
            return { error: true };
        }
    }

    static async put(url, requestBody) {
        const csrf = getCookie("csrftoken");
        const isFormData = requestBody instanceof FormData;
        let jsonBody = requestBody;
        if (isFormData) jsonBody = formDataToJSON(jsonBody);

        try {
            const res = await fetch(url, {
                method: "PUT",
                headers: {
                    "X-CSRFToken": csrf,
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                body: jsonBody
            });

            const { ok, json, sessionExpired } = await parseJSONSafe(res);
            if (!ok) {
                if (sessionExpired) return { error: true };
                return { error: true };
            }

            if (!res.ok) {
                let msg = json.error || "¡Error en la operación!";
                if (res.status >= 500) {
                    msg = "Ocurrió un error interno en el servidor al actualizar la información. Tus datos no se han perdido, por favor inténtalo nuevamente.";
                }
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
                        }).join(" | ");
                    msg = `${msg} - ${detalles}`;
                }
                Alert.warning(msg);
                return { error: true, data: json };
            }

            return { error: false, data: json };
        } catch (err) {
            handleNetworkError(err);
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

            const { ok, json, sessionExpired } = await parseJSONSafe(res);
            if (!ok) {
                if (sessionExpired) return { error: true };
                return { error: true };
            }

            if (!res.ok) {
                let msg = json.error || "¡Error en la operación!";
                if (res.status >= 500) {
                    msg = "Ocurrió un error interno en el servidor. Por favor inténtalo nuevamente.";
                }
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
            handleNetworkError(err);
            return { error: true };
        }
    }

    static async fetchGet(url) {
        try {
            const res = await fetch(url);

            const { ok, json, sessionExpired } = await parseJSONSafe(res);
            if (!ok) {
                if (sessionExpired) return { error: true };
                return { error: true };
            }

            if (!res.ok) {
                Alert.error(json.error || "¡Error en la operación!");
                return { error: true, data: json };
            }

            return { error: false, data: json };
        } catch (err) {
            handleNetworkError(err);
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

            const { ok, json, sessionExpired } = await parseJSONSafe(response);
            if (!ok) {
                if (sessionExpired) return;
                return;
            }

            if (response.ok || response.status === 404) {
                Alert.success(successText);

                if (datatableId) {
                    setTimeout(() => {
                        $(`#${datatableId}`).DataTable().ajax.reload(null, false);
                    }, 1500);
                }
            } else {
                Alert.error(json.error || errorText);
            }

        } catch (err) {
            handleNetworkError(err);
        }
    }

    static async patch(url, requestBody) {
        const csrf = getCookie("csrftoken");
        const isFormData = requestBody instanceof FormData;
        let jsonBody = requestBody;
        if (isFormData) jsonBody = formDataToJSON(jsonBody);

        try {
            const res = await fetch(url, {
                method: "PATCH",
                headers: {
                    "X-CSRFToken": csrf,
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                body: jsonBody
            });

            const { ok, json, sessionExpired } = await parseJSONSafe(res);
            if (!ok) {
                if (sessionExpired) return { error: true };
                return { error: true };
            }

            if (!res.ok) {
                let msg = json.error || "¡Error en la operación!";
                if (res.status >= 500) {
                    msg = "Ocurrió un error interno en el servidor. Por favor inténtalo nuevamente.";
                }
                Alert.error(msg);
                return { error: true, data: json };
            }

            return { error: false, data: json };
        } catch (err) {
            handleNetworkError(err);
            return { error: true };
        }
    }
}
