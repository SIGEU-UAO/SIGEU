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

        # Detect action if exists
        accion = item.get("accion", "").strip().lower()
        is_remove = accion == "eliminar"
        is_edit = accion == "actualizar"

        # Determine which required keys to validate
        keys_required = required_keys.copy()
        if is_remove and schema == SCHEMAS["organizadores_evento"]:
            keys_required.remove("aval")  # No need to validate aval when deleting

        if is_remove and schema == SCHEMAS["organizaciones_invitadas"]:
            keys_required.remove("representante_asiste")
            keys_required.remove("certificado_participacion")

        # It must have exactly the required keys.
        if not set(keys_required).issubset(keys):
            return False
        
        # There should be no keys other than those required or optional.
        allowed_keys = set(required_keys + optional_keys)
        if not keys.issubset(allowed_keys):
            return False

        # 3 Validate required types
        for k in keys_required:
            expected_type = types[k]
            value = item.get(k)
            if not validate_type(value, expected_type, is_edit):
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
        
        if not item.get("representante_asiste") and not item.get("representante_alterno") and accion != "eliminar" and schema == SCHEMAS["organizaciones_invitadas"]:
            return False
    
    return True

def validate_type(value, expected_type, is_edit=False):    
    if expected_type == int:
        return isinstance(value, int)
    elif expected_type == bool:
        return isinstance(value, bool)
    elif expected_type == str:
        return isinstance(value, str)
    elif expected_type == "file/pdf":
        if is_edit and value is None:
            return True
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
        "optional_keys": ["accion"],
        "types": { "id": int, "aval": "file/pdf", "accion": str }
    },
    "organizaciones_invitadas": {
        "required_keys": ["id", "representante_asiste", "certificado_participacion"],
        "optional_keys": ["representante_alterno", "accion"],
        "types": {
            "id": int,
            "representante_asiste": bool,
            "representante_alterno": str,
            "certificado_participacion": "file/pdf",
            "accion": str
        }
    }
}