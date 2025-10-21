class OrganizadorSerializer:
    def serialize_organizador(organizador):
        """Converts an Instalacion instance into a JSON-serializable dictionary."""
        organizador_instance = organizador.organizador

        return {
            "idOrganizador": getattr(organizador_instance, "idUsuario", None),
            "aval": organizador.aval.name if getattr(organizador, "aval", None) else None,
            "nombreCompleto": getattr(organizador_instance, "nombres", "") + " " + getattr(organizador_instance, "apellidos", ""),
            "rol": getattr(organizador_instance, "rol", ""),
        }

    def serialize_organizadores(organizadores, many=False):
        """If many=True, serializes a list of installations."""
        if many:
            return [OrganizadorSerializer.serialize_organizador(org) for org in organizadores]
        return OrganizadorSerializer.serialize_organizador(organizadores)