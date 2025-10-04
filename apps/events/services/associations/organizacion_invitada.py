from django.db import IntegrityError
from django.db.models import ObjectDoesNotExist
from ..event import EventoService
from ...models import OrganizacionesInvitadas

class OrganizacionesInvitadasService:
    @staticmethod
    def crearOrganizacionInvitada(data):
        try:
            # 1. Obtain event
            evento = EventoService.obtener_por_id(data["evento_id"])

            # 2. Create intermediate table record
            asignacion = OrganizacionesInvitadas.objects.create(evento=evento, organizacion=data["organizacion"], representante_asiste=data["representante_asiste"], representante_alterno=data["representante_alterno"], certificado_participacion=data["certificado_participacion"])
            return asignacion

        except ObjectDoesNotExist as e:
            raise ValueError("El evento o la organización externa no existen.") from e

        except IntegrityError as e:
            raise ValueError("Esta organización externa ya fue invitada a este evento.") from e

        except Exception as e:
            raise ValueError(f"Error inesperado: {e}")