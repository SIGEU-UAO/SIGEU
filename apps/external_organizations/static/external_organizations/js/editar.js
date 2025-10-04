import Alert from "/static/js/modules/classes/Alert.js";

document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector(".form");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(form);

    try {
      const response = await fetch(window.location.href, {
        method: "POST",
        headers: {
          "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
        },
        body: formData,
      });

      const result = await response.json();

      if (result.status === "success") {
        Alert.success(result.message);
      } else {
        Alert.error(result.message);

        if (result.errors) {
          for (const [field, messages] of Object.entries(result.errors)) {
            messages.forEach((msg) => {
              Alert.error(`${field}: ${msg}`);
            });
          }
        }
      }
    } catch (err) {
      Alert.error("Error de conexión con el servidor.");
      console.error("Error en fetch editar:", err);
    }
  });
});