from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import RegistroForm
from .service import OrganizacionExternaService
import json

class OrganizacionesExternasAPI:

    @csrf_exempt
    def registro(request):
        if request.method == "POST":
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Formato JSON inválido."}, status=400)

            form = RegistroForm(data)
            if form.is_valid():
                try:
                    org_id = OrganizacionExternaService.registrar(form.cleaned_data)
                    return JsonResponse({"id": org_id, "message": "Organización registrada"}, status=201)
                except ValueError as e:
                    return JsonResponse({"error": str(e)}, status=400)
            else:
                return JsonResponse({"error": form.errors}, status=400)

        return JsonResponse({"error": "Método no permitido"}, status=405)
