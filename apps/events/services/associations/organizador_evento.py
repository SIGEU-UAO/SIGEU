from django.db import IntegrityError
from django.db.models import ObjectDoesNotExist
from ..event import EventoService
from apps.users.service import UserService
from ...models import OrganizadorEvento

class OrganizadoresEventosService:
    @staticmethod
    def crearOrganizadorEvento(data):
        try:
            # 1. Obtain organizator instance
            organizador = UserService.obtener_instance_por_id(data["organizador"])

            # 2. Create intermediate table record
            asignacion = OrganizadorEvento.objects.create(evento=data["evento"], organizador=organizador, aval=data["aval"], tipo=data["tipo"])
            return asignacion
        
        except IntegrityError as e:
            raise ValueError("Este coordinador/organizador ya fue asignado a este evento.") from e

        except Exception as e:
            raise ValueError(f"Error inesperado: {e}")