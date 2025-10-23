import os
from django.conf import settings
from django.db import IntegrityError
from django.db.models import ObjectDoesNotExist
from ..event import EventoService
from ...models import OrganizadorEvento
from ...serializers.organizadorSerializer import OrganizadorSerializer

class OrganizadoresEventosService:
    @staticmethod
    def crearOrganizadorEvento(data):
        try:
            asignacion = OrganizadorEvento.objects.create(evento=data["evento"], organizador=data["organizador"], aval=data["aval"], tipo=data["tipo"])
            return asignacion
        
        except IntegrityError as e:
            raise ValueError("Este coordinador/organizador ya fue asignado a este evento.") from e
        except Exception as e:
            raise ValueError(f"Error inesperado: {e}")

    @staticmethod
    def listarOrganizadores(eventoId):
        evento = EventoService.obtener_por_id(eventoId)
        organizadores = evento.organizadores_asignados.all()
        data = OrganizadorSerializer.serialize_organizadores(organizadores, many=True, evento=evento)
        return data
    
    @staticmethod
    def actualizarOrganizadorEvento(data):
        evento = data.get("evento")
        organizador = data.get("organizador")
        aval = data.get("aval")
        tipo = data.get("tipo")

        # Display organizers registered in the database
        try:
            rel = OrganizadorEvento.objects.get(evento=evento, organizador=organizador)
        except OrganizadorEvento.DoesNotExist:
            raise ValueError(f"No se encontró el organizador '{organizador.nombres}' asignado a este evento.")

        # If there is a previous file, delete it from storage.
        if aval and rel.aval:
            old_path = rel.aval.path
            if os.path.isfile(old_path):
                os.remove(old_path)

        # Update fields
        rel.aval = aval
        rel.tipo = tipo
        rel.save()

    @staticmethod
    def eliminarOrganizadorEvento(data):
        try:
            asignacion = OrganizadorEvento.objects.get(evento=data["evento"], organizador=data["organizador"])
            
            # Delete associated file if it exists
            if asignacion.aval:
                old_path = asignacion.aval.path
                if os.path.isfile(old_path):
                    os.remove(old_path)
            
            asignacion.delete()
        except ObjectDoesNotExist:
            raise ValueError("La instalación que se pretende eliminar no está asginada al evento")
        except Exception as e:
            raise ValueError(f"Error al eliminar la instalación asignada: {e}")