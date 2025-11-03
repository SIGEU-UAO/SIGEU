import os
from django.db import IntegrityError, transaction
from django.conf import settings
from django.db import IntegrityError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from datetime import datetime
from django.utils import timezone
from apps.users.models import Usuario
from ..models import Evento, OrganizadorEvento, OrganizacionInvitada
from django.db.models import Q

class EventoService:
    @staticmethod
    def registrar(request, data):
        try:
            evento = Evento.objects.create(
                nombre=data["nombre"],
                descripcion=data["descripcion"],
                tipo=data["tipo"],
                capacidad=data["capacidad"],
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
            campos = ["nombre", "tipo", "descripcion", "capacidad", "fecha", "horaInicio", "horaFin"]
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
        
    def serializar_eventos(page_obj, request=None):
        results = []
        for e in page_obj.object_list:
            # organizadores asignados (resumido)
            organizadores = []
            for o in e.organizadores_asignados.all():
                u = o.organizador
                organizadores.append({
                    "nombre": ((getattr(u, "nombres", "") or "") + " " + (getattr(u, "apellidos", "") or "")).strip(),
                    "rol_organizador": o.get_tipo_display() if hasattr(o, "get_tipo_display") else o.tipo
                })

            # organizaciones invitadas (resumido)
            organizaciones = []
            for oi in e.organizaciones_invitadas.all():
                org = oi.organizacion
                organizaciones.append({"nombre": getattr(org, "nombre", None),"nit": getattr(org, "nit", None)})

            item = {
                "idEvento": e.idEvento,
                "nombre": e.nombre,
                "fecha": e.fecha.isoformat() if e.fecha else None,
                "horaInicio": e.horaInicio.isoformat() if e.horaInicio else None,
                "estado": e.estado,
                "instalaciones": [ getattr(a.instalacion, "nombre", str(a.instalacion)) for a in e.instalaciones_asignadas.all() ],
                "organizadores": organizadores,
                "organizaciones_invitadas": organizaciones
            }
            
            results.append(item)

        return {
            "count": page_obj.paginator.count,
            "num_pages": page_obj.paginator.num_pages,
            "current_page": page_obj.number,
            "results": results,
        }
    
    @staticmethod
    def actualizar_estado(id_evento, nuevo_estado):
        try:
            evento = Evento.objects.get(idEvento=id_evento)
            evento.estado = nuevo_estado
            evento.save()
            return True
        except Evento.DoesNotExist:
            return False
        
    @staticmethod
    def actualizar_fecha_envio(id_evento):
        try:
            evento = Evento.objects.get(idEvento=id_evento)
            evento.fechaEnvio = timezone.now()
            evento.save()
            return True
        except Evento.DoesNotExist:
            return False

    @staticmethod
    def reestablecer_a_borrador(evento):
        if evento.estado == "Rechazado":
            evento.estado = "Borrador"
            evento.save(update_fields=["estado", "fecha_ultimo_cambio"])

    @staticmethod
    def listar_eventos_enviados(facultad, page=1, per_page=12):
        qs = Evento.objects.filter(
            estado__iexact="Enviado"
        ).filter(
            Q(creador__estudiante__programa__facultad=facultad) | Q(creador__docente__unidadAcademica__facultad=facultad)
        ).order_by('fechaEnvio')

        paginator = Paginator(qs, per_page)
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        return page_obj
    
    @staticmethod
    def obtener_datos_organizador(id_evento, id_organizador):
        try:
            organizador_evento = OrganizadorEvento.objects.get(
                evento_id=id_evento,
                organizador_id=id_organizador
            )
            return {
                "organizador_evento": {
                    "aval": organizador_evento.aval.url if organizador_evento.aval else None,
                    "tipo": organizador_evento.get_tipo_display(),
                }
            }
        except OrganizadorEvento.DoesNotExist:
            return None
        
    @staticmethod
    def obtener_datos_organizacion_invitada(id_evento, id_organizacion):
        try:
            org_invitada = (OrganizacionInvitada.objects.get(
                    evento=id_evento,
                    organizacion=id_organizacion
                )
            )
            return { 
                "OrganizacionInvitada": {
                    "representante_asiste": org_invitada.representante_asiste,
                    "representante_alterno": org_invitada.representante_alterno,
                    "certificado_participacion": org_invitada.certificado_participacion.url if org_invitada.certificado_participacion else None,
                }
            }
        except OrganizacionInvitada.DoesNotExist:
            return None
        
    @staticmethod
    def eliminar_evento(id_evento):
        paths_to_delete = []

        try:
            with transaction.atomic():
                try:
                    evento = Evento.objects.select_for_update().get(idEvento=id_evento)
                except Evento.DoesNotExist:
                    raise ValueError("Evento no encontrado.")

                for o in evento.organizadores_asignados.all():
                    try:
                        if getattr(o, "aval", None) and getattr(o.aval, "name", None):
                            paths_to_delete.append(o.aval.path)
                    except Exception:
                        pass

                for oi in evento.organizaciones_invitadas.all():
                    try:
                        if getattr(oi, "certificado_participacion", None) and getattr(oi.certificado_participacion, "name", None):
                            paths_to_delete.append(oi.certificado_participacion.path)
                    except Exception:
                        pass

                evento.delete()
        except ValueError:
            raise
        except Exception as e:
            raise ValueError("Ocurrió un error al eliminar el evento en la base de datos.") from e

        failed_paths = []
        media_root = os.path.abspath(str(settings.MEDIA_ROOT))

        for path in paths_to_delete:
            try:
                abs_path = os.path.abspath(str(path))
                if not abs_path.startswith(media_root):
                    continue

                if os.path.isfile(abs_path):
                    os.remove(abs_path)
                    dirpath = os.path.dirname(abs_path)
                    while dirpath.startswith(media_root):
                        try:
                            if not os.listdir(dirpath):
                                os.rmdir(dirpath)
                                dirpath = os.path.dirname(dirpath)
                            else:
                                break
                        except OSError:
                            break

            except Exception:
                failed_paths.append(path)

        return {"deleted": True, "failed_paths": failed_paths}