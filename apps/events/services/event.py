from django.db import IntegrityError, transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
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
        qs = Evento.objects.filter(creador=usuario).order_by('-fecha_ultimo_cambio')
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
    def es_creador(usuario, id_event):
        event = EventoService.obtener_por_id(id_event)
        if not event:
            return None 
        return usuario.idUsuario == event.creador_id
    
    @staticmethod
    def actualizar(event, data):
        #Validate integrity errors for unique fields
        try:
            campos = ["nombre", "tipo", "descripcion", "fecha", "horaInicio", "horaFin"]
            cambios = {}

            for campo in campos:
                valor_actual = getattr(event, campo)
                valor_nuevo = data.get(campo)

                if str(valor_actual) != str(valor_nuevo):
                    cambios[campo] = valor_nuevo
                    
                # Normalize types
                if campo == "fecha" and isinstance(valor_nuevo, str):
                    valor_nuevo = datetime.strptime(valor_nuevo, "%Y-%m-%d").date()

                if campo in ["horaInicio", "horaFin"] and isinstance(valor_nuevo, str):
                    valor_nuevo = datetime.strptime(valor_nuevo, "%H:%M").time()

                # Compare normalized values
                if valor_actual != valor_nuevo:
                    cambios[campo] = valor_nuevo

            if not cambios:
                return None
            
            # Update only the modified fields
            for campo, valor in cambios.items():
                setattr(event, campo, valor)

            with transaction.atomic():
                event.save()

            # Update last_change_date
            
        except Evento.DoesNotExist:
            raise ValueError("No se encontró el evento especificado.")
        
        return event
    
    def actualizar_fecha_ultimo_cambio(evento):
        evento.fecha_ultimo_cambio = timezone.now()
        evento.save(update_fields=["fecha_ultimo_cambio"])