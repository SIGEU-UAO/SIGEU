class InstalacionSerializer:
    def serialize_instalacion(instalacion):
        """Converts an Instalacion instance into a JSON-serializable dictionary."""
        instalacion_instance = instalacion.instalacion

        return {
            "id_instalacion": getattr(instalacion_instance, "id_instalacion", None),
            "ubicacion": getattr(instalacion_instance, "ubicacion", ""),
            "tipo": getattr(instalacion_instance, "tipo", ""),
            "capacidad": getattr(instalacion_instance, "capacidad", None)
        }

    def serialize_instalaciones(instalaciones, many=False):
        """If many=True, serializes a list of installations."""
        if many:
            return [InstalacionSerializer.serialize_instalacion(inst) for inst in instalaciones]
        return InstalacionSerializer.serialize_instalacion(instalaciones)