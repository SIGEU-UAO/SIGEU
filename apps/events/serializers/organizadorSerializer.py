class OrganizadorSerializer:
    def serialize_organizador(organizador):
        """Converts an Organizador instance into a JSON-serializable dictionary"""
        organizador_instance = organizador.organizador

        return {
            "idOrganizador": getattr(organizador_instance, "idUsuario", None),
            "aval": organizador.aval.name if getattr(organizador, "aval", None) else None,
            "nombreCompleto": getattr(organizador_instance, "nombres", "") + " " + getattr(organizador_instance, "apellidos", ""),
            "rol": getattr(organizador_instance, "rol", ""),
        }

    def serialize_organizadores(organizadores, many=False, evento=None):
        """If many=True, serializes a list of installations"""
        if not many:
            return OrganizadorSerializer.serialize_organizador(organizadores)

        data = [OrganizadorSerializer.serialize_organizador(org) for org in organizadores]

        # If the event passes, prioritize the creator (first position)
        if evento:
            creador_id = getattr(evento.creador, "idUsuario", None)
            data.sort(key=lambda org: org["idOrganizador"] != creador_id)

        return data