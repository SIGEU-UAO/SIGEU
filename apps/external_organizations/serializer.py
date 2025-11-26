class ExternalOrganizationSerializer:
    def serialize_organization(organizacion):
        """Converts an Organization instance into a JSON-serializable dictionary."""
        return {
            "nit": getattr(organizacion, "nit", ""),
            "nombre": getattr(organizacion, "nombre", ""),
            "representanteLegal": getattr(organizacion, "representante_legal", ""),
            "telefono": getattr(organizacion, "telefono", ""),
            "ubicacion": getattr(organizacion, "ubicacion", ""),
            "sectorEconomico": getattr(organizacion, "sector_economico", ""),
            "actividadPrincipal": getattr(organizacion, "actividad_principal", ""),
        }

    def serialize_organizations(organizaciones, many=False):
        """If many=True, serializes a list of installations."""
        if many:
            return [ExternalOrganizationSerializer.serialize_organization(org) for org in organizaciones]
        return ExternalOrganizationSerializer.serialize_organization(organizaciones)