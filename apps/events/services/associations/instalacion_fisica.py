from django.db import IntegrityError
from django.db.models import ObjectDoesNotExist
from apps.events.services.event import EventoService
from ...models import Evento, InstalacionesAsignadas

class InstalacionesAsignadasService:
    @staticmethod
    def crearInstalacionAsignada(data):
        try:
            # 1. Obtain event
            evento = EventoService.obtener_por_id(data["evento_id"])

            # 2. Create intermediate table record
            asignacion = InstalacionesAsignadas.objects.create(evento=evento, instalacion=data["instalacion"])
            return True

        except ObjectDoesNotExist as e:
            raise ValueError("El evento o la instalación no existen.") from e

        except IntegrityError as e:
            raise ValueError("Esta instalación ya fue asignada a este evento.") from e