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
    def mis_eventos_api(request):
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
