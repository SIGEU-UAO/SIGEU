from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile

def validate_collection(data, schema):
    if not isinstance(data, list) or len(data) == 0:
        return False

    required_keys = schema["required_keys"]
    types = schema["types"]

    for item in data:
        if not isinstance(item, dict):
            return False

        keys = item.keys()

        # It must have exactly the required keys.
        if set(keys) != set(required_keys):
            return False

        # Each property must be of the correct type.
        for k in required_keys:
            expected_type = types[k]
            value = item.get(k)

            if expected_type == int:
                if not isinstance(value, int):
                    return False

            elif expected_type == "file/pdf":
                if not isinstance(value, UploadedFile):
                    return False
                try:
                    validate_pdf(value)
                except ValidationError:
                    return False
            else:
                if not isinstance(value, expected_type):
                    return False
    
    return True

# * Schemas for each model
SCHEMAS = {
    "instalaciones_asignadas": {
        "required_keys": ["id"],
        "types": {"id": int}
    },
    "organizadores_evento": {
        "required_keys": ["id", "aval"],
        "types": { "id": int, "aval": "file/pdf" }
    }
}

def validate_pdf(file):
    if not file.name.lower().endswith('.pdf'):
        raise ValidationError("Solo se permiten archivos PDF.")