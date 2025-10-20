from django.db import IntegrityError
from django.db.models import ObjectDoesNotExist
from ..event import EventoService
from ...models import OrganizacionInvitada

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