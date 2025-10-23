from django.http import JsonResponse
from ...services.associations.organizador_evento import OrganizadoresEventosService
from ...services.event import EventoService
from apps.users.service import UserService;
from ...validations.data_validators import validate_collection, SCHEMAS
from django.contrib.auth.decorators import login_required
from sigeu.decorators import organizador_required
    
class OrganizadorEventoAPI:
    @login_required()
    @organizador_required
    def asignar_organizadores_evento(request):
        if request.method == "POST":
            evento_id = request.POST.get("evento")
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

            ids = request.POST.getlist("organizadores_id[]")
            avales = request.FILES.getlist("organizadores_aval[]")
            
            organizadores = []
            for i in range(len(ids)):
                organizadores.append({
                    "id": int(ids[i]),          
                    "aval": avales[i]           
                })

            if not validate_collection(organizadores, SCHEMAS["organizadores_evento"]):
                return JsonResponse({ "error": "Datos de organizadores inválidos." }, status=400)

            errores = []
            guardadas = []

            # * Try to assign all facilities
            for item in organizadores:
                try:
                    organizador = UserService.obtener_instance_por_id(item["id"])
                    
                    # If the user was not found, add an error.
                    if not organizador:
                        errores.append({
                            "id": item["id"],
                            "error": "Usuario no encontrado."
                        })
                        continue

                    # If the user isn't a organizator...
                    if organizador.rol != "Estudiante" and organizador.rol != "Docente":
                        errores.append({
                            "id": item["id"],
                            "error": "El usuario no es un organizador"
                        })
                        continue

                    # Determine type of endorsement according to role
                    tipo = OrganizadorEventoAPI.getAvalType(organizador.rol)
                    OrganizadoresEventosService.crearOrganizadorEvento({ "evento": evento, "organizador": organizador, "aval":item["aval"], "tipo":tipo })
                    guardadas.append(organizador.idUsuario)
                except Exception as e:
                    # Catch any other errors
                    errores.append({
                        "id": item.get("id"),
                        "error": str(e)
                    })
                    continue

            if errores:
                return JsonResponse({
                    "error": "Error al asignar algun organizador",
                    "asignadas": guardadas,
                    "errores": errores
                }, status=207)

            return JsonResponse({
                "asignadas": guardadas,
                "message": "Organizadores asignados correctamente"
            }, status=201)

        return JsonResponse({"error": "Método no permitido"}, status=405)

    @login_required()
    @organizador_required
    def listar_organizadores(request, eventoId):
        if request.method == "GET":
            # Verify if it is the event creator
            es_creador = EventoService.es_creador(request.user, eventoId)
            if not es_creador:
                return JsonResponse({"error": "No tienes permiso para listar las instalaciones fisicas asignadas a este evento."}, status=403)
            
            return JsonResponse({ "organizadores": OrganizadoresEventosService.listarOrganizadores(eventoId) })
        return JsonResponse({"error": "Método no permitido"}, status=405)

    @login_required()
    @organizador_required
    def actualizar_organizadores(request, eventoId):
        if request.method == "POST":            
            # Get the event
            evento = EventoService.obtener_por_id(eventoId)
            if not evento:
                return JsonResponse({ "error": "El evento especificado no existe" }, status=404)

            # Verify if it is the event creator
            es_creador = EventoService.es_creador(request.user, eventoId)
            if not es_creador:
                return JsonResponse({"error": "No tienes permiso para modificar las instalaciones de este evento."}, status=403)

            ids = request.POST.getlist("organizadores_id[]")
            avales = request.FILES.getlist("organizadores_aval[]")
            acciones = request.POST.getlist("organizadores_accion[]")
            
            organizadores = []
            file_index = 0

            for i, id_str in enumerate(ids):
                accion = acciones[i].lower()
                aval = None

                if accion != "eliminar":  # Solo asignamos archivo si no es eliminar
                    aval = avales[file_index]
                    file_index += 1

                organizadores.append({
                    "id": int(id_str),          
                    "aval": aval,
                    "accion": accion           
                })

            if not validate_collection(organizadores, SCHEMAS["organizadores_evento"]):
                return JsonResponse({ "error": "Datos de instalaciones físicas inválidos." }, status=400)

            agregados = []
            actualizados = []
            eliminados = []
            errores = []

            # * Try to assign all facilities
            for item in organizadores:
                org_id = item.get("id")
                accion = (item.get("accion") or "").strip().lower()

                if not org_id or accion not in ("agregar", "eliminar", "actualizar"):
                    errores.append({"id": org_id, "error": "Formato inválido o acción no reconocida."})
                    continue

                try:
                    organizador = UserService.obtener_instance_por_id(org_id)
                    if not organizador or organizador.rol not in ("Estudiante", "Docente"):
                        errores.append({"id": org_id, "error": "Organizador no encontrada o no es organizador."})
                        continue

                    # Handle the actions
                    if accion == "agregar":
                        try:
                            tipo = OrganizadorEventoAPI.getAvalType(organizador.rol)
                            OrganizadoresEventosService.crearOrganizadorEvento({ "evento": evento, "organizador": organizador, "aval":item["aval"], "tipo":tipo })
                            agregados.append(organizador.idUsuario)
                        except Exception as e:
                            errores.append({"id": organizador.idUsuario, "error": str(e)})
                    elif accion == "actualizar":
                        try:
                            tipo = OrganizadorEventoAPI.getAvalType(organizador.rol)
                            OrganizadoresEventosService.actualizarOrganizadorEvento({ "evento": evento, "organizador": organizador, "aval":item["aval"], "tipo":tipo })
                            actualizados.append(organizador.idUsuario)
                        except Exception as e:
                            errores.append({"id": organizador.idUsuario, "error": str(e)})
                    elif accion == "eliminar":
                        try:
                            OrganizadoresEventosService.eliminarOrganizadorEvento({ "evento": evento, "organizador": organizador})
                            eliminados.append(organizador.idUsuario)
                        except Exception as e:
                            errores.append({"id": organizador.idUsuario, "error": str(e)})

                except Exception as e:
                    errores.append({"id": organizador.idUsuario, "error": str(e)})

            if errores:
                return JsonResponse({
                    "error": "Error al actualizar los organizadores del evento",
                    "agregados": agregados,
                    "actualizados": actualizados,
                    "eliminados": eliminados,
                    "errores": errores
                }, status=207)

            return JsonResponse({
                "agregados": agregados,
                "actualizados": actualizados,
                "eliminados": eliminados,
                "message": "Organizadores del evento actualizados correctamente"
            }, status=201)

        return JsonResponse({"error": "Método no permitido"}, status=405)

    def getAvalType(rol):
        return "director_programa" if rol == "Estudiante" else ("director_docencia" if rol == "Docente" else None)