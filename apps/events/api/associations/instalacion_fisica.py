from django.http import JsonResponse
from ...services.event import EventoService
from ...services.associations.instalacion_fisica import InstalacionesAsignadasService
from apps.core.service import InstalacionesFisicasService;
from ...validations.data_validators import validate_collection, SCHEMAS
from django.contrib.auth.decorators import login_required
from sigeu.decorators import organizador_required
import json

class InstalacionesAsignadasAPI:
    @login_required
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
            
            # * Verify if the sum of the capacities of the physical facilities is greater than the event capacity
            total_capacity = 0
            instalaciones_instances = []

            for item in instalaciones:
                instalacion = InstalacionesFisicasService.obtener_por_id(item["id"])

                # If the installation was not found, add an error.
                if not instalacion:
                    errores.append({ "id": item["id"], "error": "Instalación no encontrada."})
                    continue

                instalaciones_instances.append(instalacion)
                total_capacity += instalacion.capacidad
            
            if total_capacity < evento.capacidad:
                return JsonResponse({ "error": "La suma de las capacidades de las instalaciones no abarca la capacidad del evento" }, status=400)

            # * Try to assign all facilities
            for instalacion in instalaciones_instances:
                try:
                    InstalacionesAsignadasService.crearInstalacionAsignada({ "evento": evento, "instalacion": instalacion })
                    guardadas.append(instalacion.idInstalacion)

                except Exception as e:
                    # Catch any other errors
                    errores.append({
                        "id": instalacion.idInstalacion,
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
    
    @login_required
    @organizador_required
    def listar_instalaciones_asignadas(request, eventoId):
        if request.method == "GET":
            # Verify if it is the event creator
            es_creador = EventoService.es_creador(request.user, eventoId)
            if not es_creador:
                return JsonResponse({"error": "No tienes permiso para listar las instalaciones fisicas asignadas a este evento."}, status=403)
            
            return JsonResponse({ "instalaciones": InstalacionesAsignadasService.listarInstalacionesAsignadas(eventoId) })
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    @login_required
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

            # Prepare actions and validate inputs
            acciones = []  # list of dicts { instalacion, accion }
            for item in (instalaciones or []):
                try:
                    id_inst = item.get("id")
                    accion = (item.get("accion") or "agregar").strip().lower()
                    if accion not in ("agregar", "eliminar"):
                        errores.append({"id": id_inst, "error": "Formato inválido o acción no reconocida."})
                        continue

                    instalacion = InstalacionesFisicasService.obtener_por_id(id_inst)
                    if not instalacion:
                        errores.append({"id": id_inst, "error": "Instalación no encontrada."})
                        continue

                    acciones.append({"instalacion": instalacion, "accion": accion})
                except Exception as e:
                    errores.append({"id": item.get("id"), "error": str(e)})

            # If there are input errors, return them before making changes
            if errores:
                return JsonResponse({
                    "error": "Error al actualizar alguna instalación física",
                    "agregadas": agregadas,
                    "eliminadas": eliminadas,
                    "errores": errores
                }, status=207)

            # * Calculate final set of installations (existing - removed + added)
            
            # Get the ids of the current installations in the db
            actuales_ids = set(evento.instalaciones_asignadas.values_list("instalacion_id", flat=True))
            to_add = set()
            to_remove = set()
            for a in acciones:
                inst_id = a["instalacion"].idInstalacion
                if a["accion"] == "agregar":
                    to_add.add(inst_id)
                elif a["accion"] == "eliminar":
                    to_remove.add(inst_id)

            # Calculate the final set of installations (existing - removed + added), | means union
            ids_finales = (actuales_ids - to_remove) | to_add

            # Calculate total capacity of the final set of installations
            total_capacity = 0
            for idf in ids_finales:
                inst = InstalacionesFisicasService.obtener_por_id(idf)
                if inst:
                    total_capacity += inst.capacidad

            if total_capacity < evento.capacidad:
                return JsonResponse({ "error": "La suma de las capacidades de las instalaciones no abarca la capacidad del evento" }, status=400)

            # * Execute actions (add / remove)
            for a in acciones:
                instalacion = a["instalacion"]
                accion = a["accion"]
                try:
                    if accion == "agregar":
                        try:
                            InstalacionesAsignadasService.crearInstalacionAsignada({ "evento": evento, "instalacion": instalacion})
                            agregadas.append(instalacion.idInstalacion)
                        except Exception as e:
                            errores.append({"id": instalacion.idInstalacion, "error": str(e)})
                    elif accion == "eliminar":
                        try:
                            InstalacionesAsignadasService.eliminarInstalacionAsignada({ "evento": evento, "instalacion": instalacion})
                            eliminadas.append(instalacion.idInstalacion)
                        except Exception as e:
                            errores.append({"id": instalacion.idInstalacion, "error": str(e)})
                except Exception as e:
                    errores.append({"id": instalacion.idInstalacion, "error": str(e)})

            if errores:
                return JsonResponse({
                    "error": "Error al actualizar alguna instalación física",
                    "agregadas": agregadas,
                    "eliminadas": eliminadas,
                    "errores": errores
                }, status=207)
            
            if agregadas or eliminadas:
                EventoService.reestablecer_a_borrador(evento)
                EventoService.actualizar_fecha_ultimo_cambio(evento)

            return JsonResponse({
                "agregadas": agregadas,
                "eliminadas": eliminadas,
                "message": "Instalaciones físicas actualizadas correctamente"
            }, status=201)

        return JsonResponse({"error": "Método no permitido"}, status=405)