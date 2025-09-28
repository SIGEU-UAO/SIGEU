from django.http import JsonResponse
from .service import InstalacionesFisicasService
from django.contrib.auth.decorators import login_required
from sigeu.decorators import organizador_required
import json

class CoreAPI:
    @login_required()
    @organizador_required
    def listar(request):
        # Check for query parameters
        if request.method == "GET":
            if request.GET:
                ubicacionSearch = request.GET.get("q")
                if ubicacionSearch:
                    instalaciones = InstalacionesFisicasService.filtrar_por_ubicacion(ubicacionSearch)

                     # No results found
                    if not instalaciones:
                        return JsonResponse({
                            "message": "No se encontraron instalaciones físicas",
                            "messageType": "info"
                        }, status=200)
                    else:
                        # Return all the organizations
                        return JsonResponse({
                            "items": instalaciones,
                            "message": "Búsqueda completada correctamente!",
                            "messageType": "success"
                        }, status=200)
                else:
                    return JsonResponse({"error": "No se envió el query param adecuado"}, status=400)
            else:
                instalaciones = list(InstalacionesFisicasService.listar())
                return JsonResponse({"items": instalaciones}, status=200)

        return JsonResponse({"error": "Método no permitido"}, status=405)

"""
    @login_required()
    @organizador_required
    def obtener_por_id(request, id):
        if request.method == "GET":
            org = OrganizacionExternaService.obtener_por_id(id)
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
"""