from django.http import JsonResponse
from ...services.associations.organizador_evento import OrganizadoresEventosService
from apps.users.service import UserService;
from ...validations.data_validators import validate_collection, SCHEMAS
from django.contrib.auth.decorators import login_required
from sigeu.decorators import organizador_required
    
class OrganizadorEventoAPI:
    @login_required()
    @organizador_required
    def asignar_coordinadores_evento(request):
        if request.method == "POST":
            evento_id = request.POST.get("evento")

            if not evento_id:
                return JsonResponse({ "error": "No se suministró el id del evento" }, status=400)

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
                    organizador = UserService.obtener_organizador_por_id(item["id"])
                    
                    # If the user was not found, add an error.
                    if not organizador:
                        errores.append({
                            "id": item["id"],
                            "error": "Usuario no encontrada."
                        })
                        continue

                    # If the user isn't a organizator...
                    if organizador.get("rol") != "Estudiante" and organizador.get("rol") != "Docente":
                        errores.append({
                            "id": item["id"],
                            "error": "El usuario no es un organizador"
                        })
                        continue

                    # Determine type of endorsement according to role
                    if organizador.get("rol") == "Estudiante":
                        tipo = "director_programa"
                    elif organizador.get("rol") == "Docente":
                        tipo = "director_docencia"

                    creada = OrganizadoresEventosService.crearOrganizadorEvento({ "evento_id": evento_id, "organizador": organizador.get("idUsuario"), "aval":item["aval"], "tipo":tipo })
                    if creada:
                        guardadas.append(organizador.get("idUsuario"))

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