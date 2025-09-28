from django.db import IntegrityError
from ..models import Evento

class OrganizadorService:
    @staticmethod
    def registrar(request, data):
        try:
            evento = Evento.objects.create(
                nombre=data["nombre"],
                descripcion=data["descripcion"],
                tipo=data["tipo"],
                fecha=data["fecha"],
                horaInicio=data["horaInicio"],
                horaFin=data["horaFin"],
                creador=request.user
            )
        except IntegrityError as e:
            raise ValueError("Error al registar el evento.") from e

        return evento.idEvento