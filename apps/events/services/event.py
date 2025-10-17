from django.db import IntegrityError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..models import Evento


class EventoService:
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

    @staticmethod
    def obtener_por_id(id_evento):
        try:
            evento = Evento.objects.get(idEvento=id_evento)
            return evento
        except Evento.DoesNotExist:
            return False
    
    @staticmethod
    def listar_por_organizador(usuario, status=None, page=1, per_page=12):
        qs = Evento.objects.filter(organizadores_asignados__organizador=usuario).distinct().order_by('-fecha', '-horaInicio')
        if status:
            qs = qs.filter(estado__iexact=status)

        paginator = Paginator(qs, per_page)
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        return page_obj