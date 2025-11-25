from django.db import IntegrityError
from django.db.models import ObjectDoesNotExist
from ...serializers.organizacionInvitadaSerializer import OrganizacionInvitadaSerializer
from ..event import EventoService
from ...models import OrganizacionInvitada
import os
from django.core.files.uploadedfile import UploadedFile

class OrganizacionesInvitadasService:
    @staticmethod
    def crearOrganizacionInvitada(data):
        try:
            asignacion = OrganizacionInvitada.objects.create(evento=data["evento"], organizacion=data["organizacion"], representante_asiste=data["representante_asiste"], representante_alterno=data["representante_alterno"], certificado_participacion=data["certificado_participacion"])
            return asignacion

        except IntegrityError as e:
            raise ValueError("Esta organización externa ya fue invitada a este evento.") from e
        except Exception as e:
            raise ValueError(f"Error inesperado: {e}")

    @staticmethod
    def listarOrganizacionesInvitadas(eventoId):
        evento = EventoService.obtener_por_id(eventoId)
        organizaciones_invitadas = evento.organizaciones_invitadas.all()
        data = OrganizacionInvitadaSerializer.serialize_organizaciones(organizaciones_invitadas, many=True)
        return data
    
    @staticmethod
    def actualizarOrganizacionInvitada(data):
        evento = data.get("evento")
        organizacion = data.get("organizacion")
        representante_asiste = data.get("representante_asiste")
        representante_alterno = data.get("representante_alterno")
        certificado_participacion = data.get("certificado_participacion")

        # Display organizers registered in the database
        try:
            rel = OrganizacionInvitada.objects.get(evento=evento, organizacion=organizacion)
        except OrganizacionInvitada.DoesNotExist:
            raise ValueError(f"No se encontró la organización '{organizacion.nombres}' asignada a este evento.")

        # If there is a previous file, delete it from storage.
        if certificado_participacion and rel.certificado_participacion:
            old_path = rel.certificado_participacion.path
            if os.path.isfile(old_path):
                os.remove(old_path)

        # Update fields
        rel.representante_asiste = representante_asiste
        rel.representante_alterno = representante_alterno
        if isinstance(certificado_participacion, UploadedFile):
            rel.certificado_participacion = certificado_participacion
        rel.save()

    @staticmethod
    def eliminarOrganizacionInvitada(data):
        try:
            asignacion = OrganizacionInvitada.objects.get(evento=data["evento"], organizacion=data["organizacion"])
            
            # Delete associated file if it exists
            if asignacion.certificado_participacion:
                old_path = asignacion.certificado_participacion.path
                if os.path.isfile(old_path):
                    os.remove(old_path)
            
            asignacion.delete()
        except ObjectDoesNotExist:
            raise ValueError("La organización que se pretende eliminar no está asginada al evento")
        except Exception as e:
            raise ValueError(f"Error al eliminar la organización asignada: {e}")