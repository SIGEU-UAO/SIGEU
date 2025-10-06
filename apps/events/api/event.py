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