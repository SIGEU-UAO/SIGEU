from django.db import IntegrityError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
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
    def listar_por_organizador(usuario, status=None, page=1, per_page=12, search=None, search_by=None):
        qs = Evento.objects.filter(creador=usuario).order_by('-fecha', '-horaInicio')
        if status:
            qs = qs.filter(estado__iexact=status)

        if search and search_by:
            if search_by == "nombre":
                qs = qs.filter(nombre__icontains=search)
            elif search_by == "fecha":
                parsed_date = None
                for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
                    try:
                        parsed_date = datetime.strptime(search, fmt).date()
                        break
                    except Exception:
                        continue
                if parsed_date:
                    qs = qs.filter(fecha=parsed_date)
                else:
                    qs = qs.none()

        paginator = Paginator(qs, per_page)
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        return page_obj
    
    @staticmethod
    def serializar_eventos(page_obj, request=None):
        results = []
        for e in page_obj.object_list:
            item = {
                "idEvento": e.idEvento,
                "nombre": e.nombre,
                "fecha": e.fecha.isoformat() if e.fecha else None,
                "horaInicio": e.horaInicio.isoformat() if e.horaInicio else None,
                "estado": e.estado,
                "instalaciones": [ getattr(a.instalacion, "nombre", str(a.instalacion)) for a in e.instalaciones_asignadas.all() ],
            }
            # para incluir urls de archivos y si se tiene `request`, construir la url absoluta:
            # if request:
            #     item["alguna_url"] = request.build_absolute_uri(e.algun_filefield.url) if e.algun_filefield else None

            results.append(item)

        return {
            "count": page_obj.paginator.count,
            "num_pages": page_obj.paginator.num_pages,
            "current_page": page_obj.number,
            "results": results,
        }
