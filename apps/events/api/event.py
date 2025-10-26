from django.http import JsonResponse
from ..forms.event import RegistroEventoForm
from ..services.event import EventoService
from ..serializers.eventoSerializer import EventoSerializer 
from django.contrib.auth.decorators import login_required
from sigeu.decorators import organizador_required
from sigeu.decorators import secretaria_required
import json

class EventoAPI:
    @login_required()
    @organizador_required
    def registro(request):
        if request.method == "POST":
            data = json.loads(request.body)
            form = RegistroEventoForm(data)
            if form.is_valid():
                try:
                    evento_id = EventoService.registrar(request, form.cleaned_data)
                    return JsonResponse({"evento": evento_id, "message": "Evento registrado"}, status=201)
                except ValueError as e:
                    return JsonResponse({"error": str(e)}, status=400)
            else:
                return JsonResponse({"error": form.errors}, status=400)
        return JsonResponse({"error": "Método no permitido"}, status=405)
    

    @login_required()
    @organizador_required
    def mis_eventos(request):
        status = request.GET.get('status')
        page = request.GET.get('page', 1)
        search = request.GET.get('search')
        search_by = request.GET.get('search_by')

        try:
            page = int(page)
        except (TypeError, ValueError):
            page = 1

        page_obj = EventoService.listar_por_organizador(
            request.user, status=status, page=page, per_page=12, search=search, search_by=search_by
        )

        data = EventoSerializer.serialize_page(page_obj)
        return JsonResponse(data, safe=False)
    
    @login_required()
    @organizador_required
    def actualizar(request, id):
        if request.method == "PUT":
            # Get the event
            evento = EventoService.obtener_por_id(id)
            if not evento:
                return JsonResponse({ "error": "El evento especificado no existe" }, status=404)
            
            #Validates if the user is the creator of the event
            es_creador = EventoService.es_creador(request.user, id)
            if not es_creador:
                return JsonResponse({"error": "No tienes permiso para actualizar este evento."}, status=403)

            data = json.loads(request.body)
            form = RegistroEventoForm(data)
            if form.is_valid():
                try:
                    result = EventoService.actualizar(evento, form.cleaned_data)
                    if result is None:
                        return JsonResponse({"message": "Tu información está al día."}, status=200)
                    
                    return JsonResponse({"message": "Información básica del evento actualizada correctamente."}, status=200)
                except ValueError as e:
                    return JsonResponse({"error": str(e)}, status=400)
            else:
                return JsonResponse({"error": form.errors}, status=400)
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    @login_required()
    @organizador_required
    def enviar_evento_validacion(request, id_evento):
        if request.method == "PATCH":
            evento = EventoService.obtener_por_id(id_evento)
            if not evento:
                return JsonResponse({"error": "Evento no encontrado."}, status=404)
            if evento.estado != "Borrador":
                return JsonResponse({"error": "Solo los eventos en estado 'borrador' pueden ser enviados a validación."}, status=400)
            if evento.creador != request.user:
                return JsonResponse({"error": "No tienes permiso para enviar este evento a validación."}, status=403)
            if not evento.instalaciones_asignadas.exists():
                return JsonResponse({"error": "El evento debe tener al menos una instalación asignada antes de enviarlo a validación."}, status=400)
            actualizado = EventoService.actualizar_estado(id_evento, "Enviado")
            fecha = EventoService.actualizar_fecha_envio(id_evento)
            if actualizado and fecha:
                return JsonResponse({"message": "El evento ha sido enviado a validación correctamente."}, status=200)
            else:
                return JsonResponse({"error": "No se pudo actualizar el estado del evento."}, status=500)
            
    login_required()
    secretaria_required()
    def listar_eventos_enviados(request):
        if request.method == "GET":
            page = request.GET.get('page', 1)

            try:
                page = int(page)
            except (TypeError, ValueError):
                page = 1

            page_obj = EventoService.listar_eventos_enviados(             
                page=page,
                per_page=12,
                facultad=request.user.secretaria.facultad
            )

            data = EventoService.serializar_eventos(page_obj, request=request)
            return JsonResponse(data, safe=False)
        
    @login_required
    @secretaria_required
    def obtener_datos_organizador(request, id_evento, id_organizador):
        if request.method == "GET":
            try:
                datos = EventoService.obtener_datos_organizador(id_evento, id_organizador)
                if not datos:
                    return JsonResponse({"error": "Datos no encontrados."}, status=404)
                return JsonResponse({"error": False, "data": datos}, status=200)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
    
    @login_required
    @secretaria_required
    def obtener_datos_organizacion_invitada(request, id_evento, id_organizacion):
        if request.method == "GET":
            try:
                datos = EventoService.obtener_datos_organizacion_invitada(id_evento, id_organizacion)
                if not datos:
                    return JsonResponse({"error": "Datos no encontrados."}, status=404)
                return JsonResponse({"error": False, "data": datos}, status=200)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)

    @login_required()
    @organizador_required
    def eliminar_evento(request, id_evento):
        if request.method != "DELETE":
            return JsonResponse({"error": "Método no permitido"}, status=405)

        try:
            result = EventoService.eliminar_evento(id_evento)
        except ValueError as ve:
            return JsonResponse({"error": str(ve)}, status=400)
        except Exception:
            return JsonResponse({"error": "Error interno al eliminar el evento."}, status=500)
        
        if result.get("failed_paths"):
            return JsonResponse({
                "message": "Evento eliminado en base de datos, pero algunos archivos no pudieron eliminarse.",
                "failed_paths": result["failed_paths"]
            }, status=200)
        else:
            return JsonResponse({"message": "Evento eliminado correctamente."}, status=200)