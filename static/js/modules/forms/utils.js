import Alert from "../classes/Alert.js"

//* Validate fields in FormData (Reusable for all forms)
export function validarFormData(formData, rules = {}) {
  for (let [campo, valor] of formData.entries()) {
    let val = valor instanceof File ? valor : valor.trim();

    // Default validation: empty
    if (!val || (val instanceof File && !val.name)) {
      Alert.error(`El campo ${campo} es obligatorio`);
      return false;
    }

    // Additional validations defined in rules
    if (rules[campo]) {
      for (let { check, msg } of rules[campo]) {
        if (!check(val, formData)) {  // formData is passed in case you need to validate against another field
          Alert.error(msg);
          return false;
        }
      }
    }
  }
  return true;
}

//* Returns a JSON from a formData
export function formDataToJSON(formData) {
  let obj = {};
  formData.forEach((val, key) => obj[key] = val.trim());
  return JSON.stringify(obj);
}

export function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// * Convert an array of FormData into a single FormData container
export function mergeFormDataFieldsArray(records, type) {
  const bigForm = new FormData();

  records.forEach((form, i) => {
      for (const [key, value] of form.entries()) {
          // Each field is stored as records[0][key], records[1][key]...
          bigForm.append(`${type}_${key}[]`, value);
      }
  });

  return bigForm;
}

export function mergeFormDataIndexed(records, type) {
  const bigForm = new FormData();

  records.forEach((form, i) => {
    for (const [key, value] of form.entries()) {
      // Use indexes to maintain an exact relationship between fields.
      bigForm.append(`${type}[${i}][${key}]`, value);
    }
  });

  return bigForm;
}


export function handleFileInputsInfo(input, existingFile = null) {
  const fileLabel = input.closest('.form__group').querySelector('.add-file-btn');

  // Check if infoDiv already exists to avoid duplication
  let infoDiv = fileLabel.nextElementSibling;
  if (!infoDiv || !infoDiv.classList.contains('file-info')) {
    infoDiv = document.createElement('div');
    infoDiv.classList.add('file-info');
    fileLabel.insertAdjacentElement('afterend', infoDiv);
  }

  // Function to update infoDiv
  const updateInfo = (file) => {
    if (file) {
      infoDiv.innerHTML = `<i class="ri-file-check-fill"></i> ${file instanceof File ? file.name : file}`;
    } else {
      infoDiv.textContent = '';
    }
  };

  // Display existing file if passed
  if (existingFile) updateInfo(existingFile);

  // Listener for future changes
  input.addEventListener('change', () => updateInfo(input.files[0]));
}

export function cleanContainer(container){
  while (container.firstElementChild) {
    container.firstElementChild.remove();
  }
}