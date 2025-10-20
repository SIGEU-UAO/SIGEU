class InstalacionSerializer:
    def serialize_instalacion(instalacion):
        """Converts an Instalacion instance into a JSON-serializable dictionary."""
        instalacion_instance = instalacion.instalacion

        return {
            "idInstalacion": getattr(instalacion_instance, "idInstalacion", None),
            "ubicacion": getattr(instalacion_instance, "ubicacion", ""),
            "tipo": getattr(instalacion_instance, "tipo", ""),
        }

    def serialize_instalaciones(instalaciones, many=False):
        """If many=True, serializes a list of installations."""
        if many:
            return [InstalacionSerializer.serialize_instalacion(inst) for inst in instalaciones]
        return InstalacionSerializer.serialize_instalacion(instalaciones)