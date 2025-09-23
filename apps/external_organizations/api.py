from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .forms import RegistroForm
from .service import OrganizacionExternaService
from .models import OrganizacionExterna
import json

class OrganizacionesExternasAPI:
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

    def listar(request):
        if request.method == "GET":
            if request.GET:
                nitSearch = request.GET.get("nit")
                if nitSearch:
                    organizaciones = OrganizacionExternaService.filtrar_por_nit(nitSearch)
                    if not organizaciones:
                        return JsonResponse({
                            "organizaciones": organizaciones,
                            "message": "No se encontraron organizaciones externas",
                            "messageType": "info"
                        }, status=200)
                    else:
                        return JsonResponse({
                            "organizaciones": organizaciones,
                            "message": "Búsqueda completada correctamente!",
                            "messageType": "success"
                        }, status=200)
                else:
                    return JsonResponse({"error": "No se envió el query param adecuado"}, status=400)
            else:
                organizaciones = OrganizacionExternaService.listar()
                return JsonResponse({"organizaciones": organizaciones}, status=200)

        return JsonResponse({"error": "Método no permitido"}, status=405)

    def detalle(request, id):
        if request.method == "GET":
            org = get_object_or_404(OrganizacionExterna, idOrganizacion=id)
           
            data = {
                "organizacion": {  
                    "idOrganizacion": org.idOrganizacion,
                    "nit": org.nit,
                    "nombre": org.nombre,
                    "representanteLegal": org.representanteLegal,
                    "telefono": org.telefono,
                    "ubicacion": org.ubicacion,
                    "sectorEconomico": org.sectorEconomico,
                    "actividadPrincipal": org.actividadPrincipal,
                }
            }
            return JsonResponse(data, status=200)

        return JsonResponse({"error": "Método no permitido"}, status=405)
