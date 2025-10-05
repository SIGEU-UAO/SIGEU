from django.http import JsonResponse

from apps.external_organizations.models import OrganizacionExterna
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
                            "organizaciones": organizaciones,
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
            qs = (
                OrganizacionExternaService.buscar(search_value)
                if search_value
                else OrganizacionExternaService.listar()
            )

            total_records = OrganizacionExterna.objects.count()
            filtered_records = qs.count()


            # Paginación
            paginator = Paginator(qs, length)
            page_number = (start // length) + 1
            page = paginator.get_page(page_number)

            data = []
            for org in page.object_list:
                data.append({
                    "id": org.idOrganizacion,
                    "nit": org.nit,
                    "nombre": org.nombre,
                    "representanteLegal": org.representanteLegal,
                    "telefono": org.telefono,
                    "ubicacion": org.ubicacion,
                    "sectorEconomico": org.sectorEconomico,
                    "actividadPrincipal": org.actividadPrincipal,
                    "esCreador": request.user.idUsuario == org.creador_id
                })
            
            

            return JsonResponse({
                "draw": draw,
                "recordsTotal": total_records,
                "recordsFiltered": filtered_records,
                "data": data
            })

        return JsonResponse({"error": "Método no permitido"}, status=405)

    @login_required()
    @organizador_required
    def obtener_por_id(request, id):
        if request.method == "GET":
            org = OrganizacionExternaService.obtener_por_id(id)
            if not org:
                return JsonResponse({"error": "Organización no encontrada."}, status=404)
            
            data = {
                "idOrganizacion": org.idOrganizacion,
                "nit": org.nit,
                "nombre": org.nombre,
                "representanteLegal": org.representanteLegal,
                "telefono": org.telefono,
                "ubicacion": org.ubicacion,
                "sectorEconomico": org.sectorEconomico,
                "actividadPrincipal": org.actividadPrincipal,
            }
            return JsonResponse({"organizacion": data}, status=200)

        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    @login_required()
    @organizador_required
    def actualizar(request, id):
        if request.method == "PUT":
            try:
                if request.content_type == "application/json":
                    data = json.loads(request.body)
                else:
                    data = request.POST
            except json.JSONDecodeError:
                return JsonResponse({"error": "Formato JSON inválido."}, status=400)

            form = RegistroForm(data)
            if form.is_valid():
                try:
                    OrganizacionExternaService.actualizar(id, form.cleaned_data)
                    return JsonResponse({"message": "Organización actualizada correctamente."}, status=200)
                except ValueError as e:
                    return JsonResponse({"error": str(e)}, status=400)
            else:
                return JsonResponse({"error": form.errors}, status=400)

        return JsonResponse({"error": "Método no permitido"}, status=405)