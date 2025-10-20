from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile

def validate_collection(data, schema):
    if not isinstance(data, list) or len(data) == 0:
        return False

    required_keys = schema["required_keys"]
    optional_keys = schema.get("optional_keys", [])
    types = schema["types"]

    for item in data:
        if not isinstance(item, dict):
            return False

        keys = set(item.keys())

        # It must have exactly the required keys.
        if not set(required_keys).issubset(keys):
            return False
        
        # There should be no keys other than those required or optional.
        allowed_keys = set(required_keys + optional_keys)
        if not keys.issubset(allowed_keys):
            return False

        # 3 Validate required types
        for k in required_keys:
            expected_type = types[k]
            value = item.get(k)
            if not validate_type(value, expected_type):
                return False

        # Validate optionals only if they exist
        for k in optional_keys:
            if k in item and item[k] not in (None, "", []):
                expected_type = types[k]
                value = item[k]
                if not validate_type(value, expected_type):
                    return False

        # For organizations...
        if item.get("representante_asiste") and item.get("representante_alterno") and schema == SCHEMAS["organizaciones_invitadas"]:
            return False    
        
        if not item.get("representante_asiste") and not item.get("representante_alterno") and schema == SCHEMAS["organizaciones_invitadas"]:
            return False
    
    return True

def validate_type(value, expected_type):
    from django.core.files.uploadedfile import UploadedFile
    if expected_type == int:
        return isinstance(value, int)
    elif expected_type == bool:
        return isinstance(value, bool)
    elif expected_type == str:
        return isinstance(value, str)
    elif expected_type == "file/pdf":
        if not isinstance(value, UploadedFile):
            return False
        return value.name.lower().endswith(".pdf")
    return False

# * Schemas for each model
SCHEMAS = {
    "instalaciones_asignadas": {
        "required_keys": ["id"],
        "optional_keys": ["accion"],
        "types": {"id": int, "accion": str}
    },
    "organizadores_evento": {
        "required_keys": ["id", "aval"],
        "types": { "id": int, "aval": "file/pdf" }
    },
    "organizaciones_invitadas": {
        "required_keys": ["id", "representante_asiste", "certificado_participacion"],
        "optional_keys": ["representante_alterno"],
        "types": {
            "id": int,
            "representante_asiste": bool,
            "representante_alterno": str,
            "certificado_participacion": "file/pdf"
        }
    }
}