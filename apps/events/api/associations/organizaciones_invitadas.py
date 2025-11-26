from django.http import JsonResponse
from ...services.associations.organizacion_invitada import OrganizacionesInvitadasService
from apps.external_organizations.service import OrganizacionExternaService;
from ...services.event import EventoService
from ...validations.data_validators import validate_collection, SCHEMAS
from django.contrib.auth.decorators import login_required
from sigeu.decorators import organizador_required
    
class OrganizacionInvitadaAPI:
    @login_required
    @organizador_required
    def asignar_organizaciones_invitadas(request):
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
            
            # Detect how many organizations are coming according to the POST keys
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

                    creada = OrganizacionesInvitadasService.crearOrganizacionInvitada({ "evento": evento, "organizacion": organizacion, "representante_asiste":item["representante_asiste"], "representante_alterno":item["representante_alterno"], "certificado_participacion": item["certificado_participacion"] })
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
    
    @login_required
    @organizador_required
    def listar_organizaciones_invitadas(request, eventoId):
        if request.method == "GET":
            # Verify if it is the event creator
            es_creador = EventoService.es_creador(request.user, eventoId)
            if not es_creador:
                return JsonResponse({"error": "No tienes permiso para listar las instalaciones fisicas asignadas a este evento."}, status=403)
            
            return JsonResponse({ "organizaciones": OrganizacionesInvitadasService.listarOrganizacionesInvitadas(eventoId) })
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    @login_required
    @organizador_required
    def actualizar_organizaciones(request, eventoId):
        if request.method == "POST":            
            # Get the event
            evento = EventoService.obtener_por_id(eventoId)
            if not evento:
                return JsonResponse({ "error": "El evento especificado no existe" }, status=404)

            # Verify if it is the event creator
            es_creador = EventoService.es_creador(request.user, eventoId)
            if not es_creador:
                return JsonResponse({"error": "No tienes permiso para modificar las instalaciones de este evento."}, status=403)

            # Detect how many organizations are coming according to the form codes
            total = len([k for k in request.POST.keys() if k.startswith("organizaciones[") and k.endswith("[id]")])

            organizaciones = []

            for i in range(total):
                id_str = request.POST.get(f"organizaciones[{i}][id]")
                accion = (request.POST.get(f"organizaciones[{i}][accion]") or "").lower()
                
                representante_asiste = request.POST.get(f"organizaciones[{i}][representante_asiste]") == "on"
                representante_alterno = request.POST.get(f"organizaciones[{i}][representante_alterno]", "")
                certificado = None

                # Solo asignar archivo si la acción NO es eliminar
                if accion != "eliminar":
                    certificado = request.FILES.get(f"organizaciones[{i}][certificado_participacion]")

                organizaciones.append({
                    "id": int(id_str),
                    "accion": accion,
                    "representante_asiste": representante_asiste if accion != "eliminar" else False,
                    "representante_alterno": representante_alterno if accion != "eliminar" else "",
                    "certificado_participacion": certificado,
                })

            if not validate_collection(organizaciones, SCHEMAS["organizaciones_invitadas"]):
                return JsonResponse({ "error": "Datos de organizaciones invitadas inválidos." }, status=400)

            agregadas = []
            actualizadas = []
            eliminadas = []
            errores = []

            # * Try to update all organizations
            for item in organizaciones:
                org_id = item.get("id")
                accion = (item.get("accion") or "").strip().lower()

                if not org_id or accion not in ("agregar", "eliminar", "actualizar"):
                    errores.append({"id": org_id, "error": "Formato inválido o acción no reconocida."})
                    continue

                try:
                    organizacion = OrganizacionExternaService.obtener_por_id(org_id)
                    if not organizacion:
                        errores.append({"id": org_id, "error": "Organización Externa no encontrada."})
                        continue

                    # Handle the actions
                    if accion == "agregar":
                        try:
                            OrganizacionesInvitadasService.crearOrganizacionInvitada({ "evento": evento, "organizacion": organizacion, "representante_asiste":item["representante_asiste"], "representante_alterno":item["representante_alterno"], "certificado_participacion":item["certificado_participacion"] })
                            agregadas.append(organizacion.id_organizacion)
                        except Exception as e:
                            errores.append({"id": organizacion.id_organizacion, "error": str(e)})
                    elif accion == "actualizar":
                        try:
                            OrganizacionesInvitadasService.actualizarOrganizacionInvitada({ "evento": evento, "organizacion": organizacion, "representante_asiste":item["representante_asiste"], "representante_alterno":item["representante_alterno"], "certificado_participacion":item["certificado_participacion"] })
                            actualizadas.append(organizacion.id_organizacion)
                        except Exception as e:
                            errores.append({"id": organizacion.id_organizacion, "error": str(e)})
                    elif accion == "eliminar":
                        try:
                            OrganizacionesInvitadasService.eliminarOrganizacionInvitada({ "evento": evento, "organizacion": organizacion})
                            eliminadas.append(organizacion.id_organizacion)
                        except Exception as e:
                            errores.append({"id": organizacion.id_organizacion, "error": str(e)})

                except Exception as e:
                    errores.append({"id": organizacion.id_organizacion, "error": str(e)})

            if errores:
                return JsonResponse({
                    "error": "Error al actualizar las organizaciones externas invitadas al evento",
                    "agregadas": agregadas,
                    "actualizadas": actualizadas,
                    "eliminadas": eliminadas,
                    "errores": errores
                }, status=207)
            
            if agregadas or actualizadas or eliminadas:
                EventoService.reestablecer_a_borrador(evento)
                EventoService.actualizar_fecha_ultimo_cambio(evento)

            return JsonResponse({
                "agregadas": agregadas,
                "actualizadas": actualizadas,
                "eliminadas": eliminadas,
                "message": "Organizaciones invitadas del evento actualizados correctamente"
            }, status=201)

        return JsonResponse({"error": "Método no permitido"}, status=405)