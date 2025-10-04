from django.http import JsonResponse
from ...services.associations.organizacion_invitada import OrganizacionesInvitadasService
from apps.external_organizations.service import OrganizacionExternaService;
from ...validations.data_validators import validate_collection, SCHEMAS
from django.contrib.auth.decorators import login_required
from sigeu.decorators import organizador_required
    
class OrganizacionInvitadaAPI:
    @login_required()
    @organizador_required
    def asignar_organizaciones_invitadas(request):
        if request.method == "POST":
            evento_id = request.POST.get("evento")

            if not evento_id:
                return JsonResponse({ "error": "No se suministró el id del evento" }, status=400)
            
            # Detectar cuántas organizaciones vienen según las claves del POST
            total = len([k for k in request.POST.keys() if k.startswith("organizaciones[") and k.endswith("[id]")])

            errores = []
            guardadas = []
            
            organizaciones = [
                {
                    "id": int(request.POST.get(f"organizaciones[{i}][id]")),
                    "representante_asiste": request.POST.get(f"organizaciones[{i}][representante_asiste]") == "on",
                    "representante_alterno": request.POST.get(f"organizaciones[{i}][representante_alterno]", ""),
                    "certificado_participacion": request.FILES.get(f"organizaciones[{i}][certificado_participacion]")
                }
                for i in range(total)
            ]

            if not validate_collection(organizaciones, SCHEMAS["organizaciones_invitadas"]):
                return JsonResponse({ "error": "Datos de organizaciones inválidos." }, status=400)

            # * Try to assign all facilities
            for item in organizaciones:
                try:
                    organizacion = OrganizacionExternaService.obtener_por_id(item["id"])
                    
                    # If the user was not found, add an error.
                    if not organizacion:
                        errores.append({
                            "id": item["id"],
                            "error": "Organización no encontrada."
                        })
                        continue

                    creada = OrganizacionesInvitadasService.crearOrganizacionInvitada({ "evento_id": evento_id, "organizacion": organizacion, "representante_asiste":item["representante_asiste"], "representante_alterno":item["representante_alterno"], "certificado_participacion": item["certificado_participacion"] })
                    if creada:
                        guardadas.append(item["id"])

                except Exception as e:
                    # Catch any other errors
                    errores.append({
                        "id": item.get("id"),
                        "error": str(e)
                    })
                    continue

            if errores:
                return JsonResponse({
                    "error": "Error al asignar alguna organización externa",
                    "asignadas": guardadas,
                    "errores": errores
                }, status=207)

            return JsonResponse({
                "asignadas": guardadas,
                "message": "Organizaciones asignadas correctamente"
            }, status=201)

        return JsonResponse({"error": "Método no permitido"}, status=405)