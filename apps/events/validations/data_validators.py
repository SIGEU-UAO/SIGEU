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
            if not isinstance(item.get(k), types[k]):
                return False
    return True


# * Schemas for each model
SCHEMAS = {
    "instalaciones_asignadas": {
        "required_keys": ["id"],
        "types": {"id": int}
    }
}