from django.db import IntegrityError
from django.db.models import ObjectDoesNotExist
from apps.core.serializers.instalacion_serializer import InstalacionSerializer
from apps.events.services.event import EventoService
from ...models import InstalacionAsignada

class InstalacionesAsignadasService:
    @staticmethod
    def crearInstalacionAsignada(data):
        try:
            asignacion = InstalacionAsignada.objects.create(evento=data["evento"], instalacion=data["instalacion"])
        except IntegrityError as e:
            raise ValueError("Esta instalación ya fue asignada a este evento.") from e
        except Exception as e:
            raise ValueError(f"Error inesperado: {e}")
        
    @staticmethod
    def listarInstalacionesAsignadas(eventoId):
        evento = EventoService.obtener_por_id(eventoId)
        instalaciones = evento.instalaciones_asignadas.all()
        data = InstalacionSerializer.serialize_instalaciones(instalaciones, many=True)
        return data
    
    @staticmethod
    def eliminarInstalacionAsignada(data):
        try:
            asignacion = InstalacionAsignada.objects.get(evento=data["evento"], instalacion=data["instalacion"])
            asignacion.delete()
        except ObjectDoesNotExist:
            raise ValueError("La instalación que se pretende eliminar no está asginada al evento")
        except Exception as e:
            raise ValueError(f"Error al eliminar la instalación asignada: {e}")