from django.http import JsonResponse
from .forms import RegistroForm
from .service import OrganizacionExternaService
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from sigeu.decorators import organizador_required
import json

class OrganizacionesExternasAPI:
    @login_required()
    @organizador_required
    def registro(request):
        if request.method == "POST":
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Formato JSON inválido."}, status=400)

            form = RegistroForm(data)
            if form.is_valid():
                try:
                    org_id = OrganizacionExternaService.registrar(request, form.cleaned_data)
                    return JsonResponse({"id": org_id, "message": "Organización registrada"}, status=201)
                except ValueError as e:
                    return JsonResponse({"error": str(e)}, status=400)
            else:
                return JsonResponse({"error": form.errors}, status=400)

        return JsonResponse({"error": "Método no permitido"}, status=405)

    @login_required()
    @organizador_required
    def listar(request):
        # Check for query parameters
        if request.method == "GET":
            if request.GET:
                nitSearch = request.GET.get("q")
                if nitSearch:
                    organizaciones = OrganizacionExternaService.filtrar_por_nit(nitSearch)

                     # No results found
                    if not organizaciones:
                        return JsonResponse({
                            "message": "No se encontraron organizaciones externas",
                            "messageType": "info"
                        }, status=200)
                    else:
                        # Return all the organizations
                        return JsonResponse({
                            "items": organizaciones,
                            "message": "Búsqueda completada correctamente!",
                            "messageType": "success"
                        }, status=200)
                else:
                    return JsonResponse({"error": "No se envió el query param adecuado"}, status=400)
            else:
                organizaciones = list(OrganizacionExternaService.listar())
                return JsonResponse({"items": organizaciones}, status=200)

        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    @login_required()
    @organizador_required
    def datatables_rendering(request):
        if request.method == "GET":
            # Datatables parameters
            draw = int(request.GET.get("draw", 1))
            start = int(request.GET.get("start", 0))
            length = int(request.GET.get("length", 10))
            search_value = request.GET.get("search[value]", "")

            # Query base
            qs = OrganizacionExternaService.listar()

            # Filtro búsqueda
            if search_value:
                qs = qs.filter(nombre__icontains=search_value)

            total = qs.count()

            # Paginación
            paginator = Paginator(qs, length)
            page_number = (start // length) + 1
            page = paginator.get_page(page_number)

            data = []
            for org in page.object_list:
                data.append({
                    "id": org["idOrganizacion"],
                    "nit": org["nit"],
                    "nombre": org["nombre"],
                    "representanteLegal": org["representanteLegal"],
                    "telefono": org["telefono"],
                    "ubicacion": org["ubicacion"],
                    "sectorEconomico": org["sectorEconomico"],
                    "actividadPrincipal": org["actividadPrincipal"],
                    "esCreador": request.user.idUsuario == org["creador_id"]
                })

            return JsonResponse({
                "draw": draw,
                "recordsTotal": total,
                "recordsFiltered": total,
                "data": data
            })

        return JsonResponse({"error": "Método no permitido"}, status=405)

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