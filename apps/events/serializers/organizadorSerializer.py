class OrganizadorSerializer:
    def serialize_organizador(organizador):
        """Converts an Organizador instance into a JSON-serializable dictionary"""
        organizador_instance = organizador.organizador

        return {
            "id_organizador": getattr(organizador_instance, "id_usuario", None),
            "aval": organizador.aval.name if getattr(organizador, "aval", None) else None,
            "nombreCompleto": getattr(organizador_instance, "nombres", "") + " " + getattr(organizador_instance, "apellidos", ""),
            "rol": getattr(organizador_instance, "rol", ""),
        }

    def serialize_organizadores(organizadores, many=False):
        """If many=True, serializes a list of installations"""
        if not many:
            return OrganizadorSerializer.serialize_organizador(organizadores)

        return [OrganizadorSerializer.serialize_organizador(org) for org in organizadores]