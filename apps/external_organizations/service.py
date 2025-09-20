from django.db import IntegrityError
from .models import *

class OrganizacionExternaService:
    @staticmethod
    def registrar(data):
        try:
            org = OrganizacionExterna.objects.create(
                nombre=data["nombre"],
                representanteLegal=data["representante_legal"],
                telefono=data["telefono"],
                ubicacion=data["ubicacion"],
                sectorEconomico=data["sector_economico"],
                actividadPrincipal=data["actividad_principal"],
            )
        except IntegrityError as e:
            s = str(e).lower()
            if "nombre" in s:
                raise ValueError("Ya existe una organización con este nombre.") from e
            raise ValueError("Error de integridad en el registro de organización.") from e

        return org.idOrganizacion
