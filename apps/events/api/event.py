from django.http import JsonResponse
from ..forms.event import RegistroEventoForm
from ..services.event import EventoService
from ..serializers.eventoSerializer import EventoSerializer 
from django.contrib.auth.decorators import login_required
from sigeu.decorators import organizador_required
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
            if not EventoService.obtener_por_id(id):
                return JsonResponse({ "error": "El evento especificado no existe" }, status=404)
            
            #Validates if the user is the creator of the event
            es_creador = EventoService.es_creador(request.user, id)
            if not es_creador:
                return JsonResponse({"error": "No tienes permiso para actualizar este evento."}, status=403)

            data = json.loads(request.body)
            form = RegistroEventoForm(data)
            if form.is_valid():
                try:
                    EventoService.actualizar(id, form.cleaned_data)
                    return JsonResponse({"message": "Información básica del evento actualizada correctamente."}, status=200)
                except ValueError as e:
                    return JsonResponse({"error": str(e)}, status=400)
            else:
                return JsonResponse({"error": form.errors}, status=400)
        return JsonResponse({"error": "Método no permitido"}, status=405)