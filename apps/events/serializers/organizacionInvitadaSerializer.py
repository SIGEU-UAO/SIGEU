class OrganizacionInvitadaSerializer:
    def serialize_organizacion(organizacion):
        """Converts an Organizacion Externa instance into a JSON-serializable dictionary"""
        organizacion_instance = organizacion.organizacion

        return {
            "idOrganizacion": getattr(organizacion_instance, "idOrganizacion", None),
            "representante_asiste": getattr(organizacion, "representante_asiste", None),
            "representante_alterno": getattr(organizacion, "representante_alterno", None),
            "certificado_participacion": organizacion.certificado_participacion.name if getattr(organizacion, "certificado_participacion", None) else None,
            "nombre": getattr(organizacion_instance, "nombre", ""),
            "nit": getattr(organizacion_instance, "nit", ""),
        }

    def serialize_organizaciones(organizadores, many=False):
        """If many=True, serializes a list of installations"""
        if many:
            return [OrganizacionInvitadaSerializer.serialize_organizacion(org) for org in organizadores]
        return OrganizacionInvitadaSerializer.serialize_organizacion(organizadores)