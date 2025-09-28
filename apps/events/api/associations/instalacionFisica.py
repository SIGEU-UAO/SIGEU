from django.http import JsonResponse
from ...services.associations.instalacionFisica import InstalacionesAsignadasService
from apps.core.service import InstalacionesFisicasService;
from ...validations.data_validators import validate_collection, SCHEMAS
from django.contrib.auth.decorators import login_required
from sigeu.decorators import organizador_required
import json

class InstalacionesAsignadasAPI:
    @login_required()
    @organizador_required
    def asignar_instalaciones_fisicas(request):
        if request.method == "POST":
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Formato JSON inválido."}, status=400)
                
            evento_id = data.get("evento")
            instalaciones = data.get("records")

            if not validate_collection(instalaciones, SCHEMAS["instalaciones_asignadas"]):
                return JsonResponse({ "error": "Datos de instalaciones físicas inválidos." }, status=400)

            errores = []
            guardadas = []

            # * Try to assign all facilities
            for item in instalaciones:
                try:
                    instalacion = InstalacionesFisicasService.obtener_por_id(item["id"])
                    
                    # If the installation was not found, add an error.
                    if not instalacion:
                        errores.append({
                            "instalacion_id": item["id"],
                            "error": "Instalación no encontrada."
                        })
                        continue

                    creada = InstalacionesAsignadasService.crearInstalacionAsignada({ "evento_id": evento_id, "instalacion_id": instalacion.idInstalacion })
                    if creada:
                        guardadas.append(instalacion.idInstalacion)

                except Exception as e:
                    # Catch any other errors
                    errores.append({
                        "instalacion_id": item.get("id"),
                        "error": str(e)
                    })
                    continue
            
            if errores:
                return JsonResponse({
                    "error": "Error al asignar alguna instalación física",
                    "asignadas": guardadas,
                    "errores": errores
                }, status=207)

            return JsonResponse({
                "asignadas": guardadas,
                "message": "Instalaciones físicas asignadas correctamente"
            }, status=201)

        return JsonResponse({"error": "Método no permitido"}, status=405)