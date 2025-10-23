from django.db.models import Q
from django.db import IntegrityError
from .models import OrganizacionExterna
from .serializer import ExternalOrganizationSerializer

class OrganizacionExternaService:
    @staticmethod
    def registrar(request, data):
        try:
            org = OrganizacionExterna.objects.create(
                nit=data["nit"],
                nombre=data["nombre"],
                representanteLegal=data["representante_legal"],
                telefono=data["telefono"],
                ubicacion=data["ubicacion"],
                sectorEconomico=data["sector_economico"],
                actividadPrincipal=data["actividad_principal"],
                creador=request.user
            )
        except IntegrityError as e:
            s = str(e).lower()
            if "nombre" in s:
                raise ValueError("Ya existe una organización con este nombre.") from e
            raise ValueError("Error de integridad en el registro de organización.") from e

        return org.idOrganizacion

    @staticmethod
    def contar():
        return OrganizacionExterna.objects.count()
    
    @staticmethod
    def listar():
        return OrganizacionExterna.objects.all()
    
    @staticmethod
    def listar_json():
        return ExternalOrganizationSerializer.serialize_organizations(OrganizacionExterna.objects.all(), many=True)
    
    @staticmethod
    def buscar(termino):
        qs = OrganizacionExterna.objects.all()
        if termino:
            qs = qs.filter(
                Q(nombre__icontains=termino)
                | Q(nit__icontains=termino)
                | Q(representanteLegal__icontains=termino)
                | Q(sectorEconomico__icontains=termino)
            )
        return qs

    @staticmethod
    def es_creador(usuario, id_org):
        org = OrganizacionExternaService.obtener_por_id(id_org)
        if not org:
            return None 
        return usuario.idUsuario == org.creador_id
    
    @staticmethod
    def filtrar_por_nit(nit):
        if not nit:
            return []
        return list(
            OrganizacionExterna.objects
            .filter(nit__icontains=nit)  
            .values(
                "idOrganizacion",   
                "nit",
                "nombre",
                "representanteLegal"
            )
        )
        
    @staticmethod
    def obtener_por_id(id_organizacion):
        try:
            return OrganizacionExterna.objects.get(idOrganizacion=id_organizacion)
        except OrganizacionExterna.DoesNotExist:
            return False
    
    @staticmethod
    def actualizar(id, data):
        #Validate integrity errors for unique fields
        try:
            org = OrganizacionExterna.objects.get(pk=id)
            org.nit = data["nit"]
            org.nombre = data["nombre"]
            org.representanteLegal = data["representante_legal"]
            org.telefono = data["telefono"]
            org.ubicacion = data["ubicacion"]
            org.sectorEconomico = data["sector_economico"]
            org.actividadPrincipal = data["actividad_principal"]
            org.save()
        except OrganizacionExterna.DoesNotExist:
            raise ValueError("No se encontró la organización especificada.")
        except IntegrityError as e:
            s = str(e).lower()
            if "nit" in s:
                raise ValueError("Ya existe una organización con este NIT.") from e
            if "telefono" in s:
                raise ValueError("Ya existe una organización con este teléfono.") from e
            raise ValueError("Error de integridad al actualizar la organización.") from e
        return org
    
    @staticmethod
    def eliminar(pk):
        try:
            organizacion = OrganizacionExterna.objects.get(pk=pk)
            organizacion.delete()
            return {"error": False, "mensaje": "Organización eliminada correctamente."}
        except OrganizacionExterna.DoesNotExist:
            return {"error": True, "mensaje": "La organización no existe."}
        except IntegrityError as e:
            return {"error": True, "mensaje": f"No se puede eliminar la organización: {str(e)}"}
        except Exception as e:
            return {"error": True, "mensaje": f"Error interno: {str(e)}"}
    