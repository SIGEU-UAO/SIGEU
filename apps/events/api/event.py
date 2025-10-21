from django.http import JsonResponse
from ..forms.event import RegistroEventoForm
from ..services.event import EventoService
from django.contrib.auth.decorators import login_required
from sigeu.decorators import organizador_required
import json

class EventoAPI:
    @login_required()
    @organizador_required
    def registro(request):
        if request.method == "POST":
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Formato JSON inválido."}, status=400)

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

        data = EventoService.serializar_eventos(page_obj, request=request)
        return JsonResponse(data, safe=False)

    @login_required()
    @organizador_required
    def actualizar_estado_evento(request, id_evento):
        if request.method == "PUT":
            try:
                data = json.loads(request.body)
                nuevo_estado = data.get("estado")
                if not nuevo_estado:
                    return JsonResponse({"error": "El nuevo estado es requerido."}, status=400)
                actualizado = EventoService.actualizar_estado(id_evento, nuevo_estado)
                if actualizado:
                    return JsonResponse({"message": "Estado del evento actualizado."}, status=200)
                else:
                    return JsonResponse({"error": "Evento no encontrado."}, status=404)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Formato JSON inválido."}, status=400)
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    @login_required()
    @organizador_required
    def enviar_evento_validacion(request, id_evento):
        if request.method == "POST":
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
            if actualizado:
                return JsonResponse({"message": "El evento ha sido enviado a validación correctamente."}, status=200)
            else:
                return JsonResponse({"error": "No se pudo actualizar el estado del evento."}, status=500)