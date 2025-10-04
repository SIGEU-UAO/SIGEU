from django.db import IntegrityError
from django.db.models import ObjectDoesNotExist
from ..event import EventoService
from apps.users.service import UserService
from ...models import OrganizadoresEventos

class OrganizadoresEventosService:
    @staticmethod
    def crearOrganizadorEvento(data):
        try:
            # 1. Obtain event & organizator
            evento = EventoService.obtener_por_id(data["evento_id"])
            organizador = UserService.obtener_instance_por_id(data["organizador"])

            # 2. Create intermediate table record
            asignacion = OrganizadoresEventos.objects.create(evento=evento, organizador=organizador, aval=data["aval"], tipo=data["tipo"])
            return asignacion

        except ObjectDoesNotExist as e:
            raise ValueError("El evento o el coordinador/organizador de evento no existen.") from e

        except IntegrityError as e:
            raise ValueError("Este coordinador/organizador ya fue asignado a este evento.") from e

        except Exception as e:
            raise ValueError(f"Error inesperado: {e}")