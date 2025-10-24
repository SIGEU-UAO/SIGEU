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
            data = json.loads(request.body)
                
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
                        errores.append({ "id": item["id"], "error": "Instalación no encontrada."})
                        continue

                    InstalacionesAsignadasService.crearInstalacionAsignada({ "evento": evento, "instalacion": instalacion })
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
    
    @login_required()
    @organizador_required
    def listar_instalaciones_asignadas(request, eventoId):
        if request.method == "GET":
            # Verify if it is the event creator
            es_creador = EventoService.es_creador(request.user, eventoId)
            if not es_creador:
                return JsonResponse({"error": "No tienes permiso para listar las instalaciones fisicas asignadas a este evento."}, status=403)
            
            return JsonResponse({ "instalaciones": InstalacionesAsignadasService.listarInstalacionesAsignadas(eventoId) })
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    @login_required()
    @organizador_required
    def actualizar_instalaciones_fisicas(request, eventoId):
        if request.method == "PUT":
            data = json.loads(request.body)
            
            # Get the event
            evento = EventoService.obtener_por_id(eventoId)
            if not evento:
                return JsonResponse({ "error": "El evento especificado no existe" }, status=404)

            # Verify if it is the event creator
            es_creador = EventoService.es_creador(request.user, eventoId)
            if not es_creador:
                return JsonResponse({"error": "No tienes permiso para modificar las instalaciones de este evento."}, status=403)
            
            instalaciones = data.get("records")

            if not validate_collection(instalaciones, SCHEMAS["instalaciones_asignadas"]):
                return JsonResponse({ "error": "Datos de instalaciones físicas inválidos." }, status=400)

            agregadas = []
            eliminadas = []
            errores = []

            # * Try to assign all facilities
            for item in instalaciones:
                inst_id = item.get("id")
                accion = (item.get("accion") or "").strip().lower()

                if not inst_id or accion not in ("agregar", "eliminar"):
                    errores.append({"id": inst_id, "error": "Formato inválido o acción no reconocida."})
                    continue

                try:
                    instalacion = InstalacionesFisicasService.obtener_por_id(inst_id)
                    if not instalacion:
                        errores.append({"id": inst_id, "error": "Instalación no encontrada."})
                        continue

                    # Handle the actions
                    if accion == "agregar":
                        try:
                            InstalacionesAsignadasService.crearInstalacionAsignada({ "evento": evento, "instalacion": instalacion})
                            agregadas.append(instalacion.idInstalacion)
                        except Exception as e:
                            errores.append({"id": inst_id, "error": str(e)})
                    elif accion == "eliminar":
                        try:
                            InstalacionesAsignadasService.eliminarInstalacionAsignada({ "evento": evento, "instalacion": instalacion})
                            eliminadas.append(instalacion.idInstalacion)
                        except Exception as e:
                            errores.append({"id": inst_id, "error": str(e)})

                except Exception as e:
                    errores.append({"id": inst_id, "error": str(e)})

            if errores:
                return JsonResponse({
                    "error": "Error al actualizar alguna instalación física",
                    "agregadas": agregadas,
                    "eliminadas": eliminadas,
                    "errores": errores
                }, status=207)
            
            if agregadas or eliminadas:
                EventoService.actualizar_fecha_ultimo_cambio(evento)

            return JsonResponse({
                "agregadas": agregadas,
                "eliminadas": eliminadas,
                "message": "Instalaciones físicas actualizadas correctamente"
            }, status=201)

        return JsonResponse({"error": "Método no permitido"}, status=405)