from django.db.models import Q
from django.db import IntegrityError

from apps.events.models import Evento, OrganizacionExterna, OrganizacionInvitada
from .serializer import ExternalOrganizationSerializer

class OrganizacionExternaService:
    @staticmethod
    def registrar(request, data):
        #Validate integrity errors for unique fields
        if OrganizacionExterna.objects.filter(nit=data["nit"]).exists():
            raise ValueError("Ya existe una organización con este NIT.")
        
        if OrganizacionExterna.objects.filter(telefono=data["telefono"]).exists():
            raise ValueError("El teléfono ya se encuentra registrado en otra organización.")

        try:
            org = OrganizacionExterna.objects.create(
                nit=data["nit"],
                nombre=data["nombre"],
                representante_legal=data["representante_legal"],
                telefono=data["telefono"],
                ubicacion=data["ubicacion"],
                sector_economico=data["sector_economico"],
                actividad_principal=data["actividad_principal"],
                creador=request.user
            )
        except IntegrityError as e:
            raise ValueError("Error de integridad en el registro de organización.") from e

        return org.id_organizacion

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
                | Q(representante_legal__icontains=termino)
                | Q(sector_economico__icontains=termino)
            )
        return qs

    @staticmethod
    def es_creador(usuario, id_org):
        org = OrganizacionExternaService.obtener_por_id(id_org)
        if not org:
            return None 
        return usuario.id_usuario == org.creador_id
    
    @staticmethod
    def filtrar_por_nit(nit):
        if not nit:
            return []
        return list(
            OrganizacionExterna.objects
            .filter(nit__icontains=nit)  
            .values(
                "id_organizacion",   
                "nit",
                "nombre",
                "representante_legal"
            )
        )
        
    @staticmethod
    def obtener_por_id(id_organizacion):
        try:
            return OrganizacionExterna.objects.get(id_organizacion=id_organizacion)
        except OrganizacionExterna.DoesNotExist:
            return False
    
    @staticmethod
    def actualizar(id, data):
        try:
            org = OrganizacionExterna.objects.get(pk=id)

            #Validate integrity errors for unique fields
            if OrganizacionExterna.objects.filter(nit=data["nit"]).exclude(pk=id).exists():
                raise ValueError("Ya existe una organización con este NIT.")
            
            if OrganizacionExterna.objects.filter(telefono=data["telefono"]).exclude(pk=id).exists():
                raise ValueError("El teléfono ya se encuentra registrado en otra organización.")

            org.nit = data["nit"]
            org.nombre = data["nombre"]
            org.representante_legal = data["representante_legal"]
            org.telefono = data["telefono"]
            org.ubicacion = data["ubicacion"]
            org.sector_economico = data["sector_economico"]
            org.actividad_principal = data["actividad_principal"]
            org.save()

            return org

        except OrganizacionExterna.DoesNotExist:
            raise ValueError("No se encontró la organización especificada.")
        except IntegrityError as e:
            raise ValueError("Error de integridad al actualizar la organización.") from e
    
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
    
    @staticmethod
    def esta_asociada_evento(org_id):
        return OrganizacionInvitada.objects.filter(organizacion_id = org_id).exists()