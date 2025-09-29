from django.db import IntegrityError
from django.db.models import ObjectDoesNotExist
from ...models import Evento, InstalacionesAsignadas
from apps.core.models import InstalacionFisica

class InstalacionesAsignadasService:
    @staticmethod
    def crearInstalacionAsignada(data):
        try:
            # 1. Obtain event and site installation
            evento = Evento.objects.get(pk=data["evento_id"])
            instalacion = InstalacionFisica.objects.get(pk=data["instalacion_id"])

            # 2. Create intermediate table record
            asignacion = InstalacionesAsignadas.objects.create(evento=evento, instalacion=instalacion)
            return True

        except ObjectDoesNotExist as e:
            raise ValueError("El evento o la instalación no existen.") from e

        except IntegrityError as e:
            raise ValueError("Esta instalación ya fue asignada a este evento.") from e