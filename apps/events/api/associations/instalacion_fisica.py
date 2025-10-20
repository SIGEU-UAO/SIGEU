from django.http import JsonResponse
from ...services.event import EventoService
from ...services.associations.instalacion_fisica import InstalacionesAsignadasService
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
            if not evento_id:
                return JsonResponse({ "error": "No se suministró el id del evento" }, status=400)
            
            # Get the event
            evento = EventoService.obtener_por_id(evento_id)
            if not evento:
                return JsonResponse({ "error": "El evento especificado no existe" }, status=404)

            # Verify if it is the event creator
            es_creador = EventoService.es_creador(request.user, evento_id)
            if not es_creador:
                return JsonResponse({"error": "No tienes permiso para asignar una instalación en este evento."}, status=403)
            
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
                            "id": item["id"],
                            "error": "Instalación no encontrada."
                        })
                        continue

                    creada = InstalacionesAsignadasService.crearInstalacionAsignada({ "evento": evento, "instalacion": instalacion })
                    if creada:
                        guardadas.append(instalacion.idInstalacion)

                except Exception as e:
                    # Catch any other errors
                    errores.append({
                        "id": item.get("id"),
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
    
    def listar_instalaciones_asignadas(request, eventoId):
        if request.method == "GET":
            # Verify if it is the event creator
            es_creador = EventoService.es_creador(request.user, eventoId)
            if not es_creador:
                return JsonResponse({"error": "No tienes permiso para listar las instalaciones fisicas asignadas a este evento."}, status=403)
            
            return JsonResponse({ "instalaciones": InstalacionesAsignadasService.listarInstalacionesAsignadas(eventoId) })
        return JsonResponse({"error": "Método no permitido"}, status=405)