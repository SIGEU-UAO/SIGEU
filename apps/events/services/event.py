import os
import logging
from django.db import IntegrityError, transaction
from django.conf import settings
from django.db import IntegrityError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from ..models import Evento

logger = logging.getLogger(__name__)

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
            logger.exception(f"Error al eliminar evento {id_evento} en la base de datos: {e}")
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
                else:
                    logger.info(f"Archivo no encontrado: {abs_path}")

            except Exception as ex:
                logger.error(f"Error al eliminar archivo {path}: {ex}")
                failed_paths.append(path)

        return {"deleted": True, "failed_paths": failed_paths}
