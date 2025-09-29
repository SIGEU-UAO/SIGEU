from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from .service import UserService
from django.contrib.auth.decorators import login_required
import json

class UsersAPI():
    def registro(request):
        if request.method == "POST":
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Formato JSON inválido."}, status=400)

            rol = data.get("rol")

            registro = {
                "email": data.get("email"),
                "password": data.get("password1"),
                "nombres": data.get("nombre"),
                "apellidos": data.get("apellido"),
                "telefono": data.get("telefono"),
                "numeroIdentificacion": data.get("documento"),
                "rol": rol,
            }

            if rol == "estudiante":
                registro["codigo_estudiante"] = data.get("codigo_estudiante")
                registro["programa_id"] = data.get("programa")
            elif rol == "docente":
                registro["unidad_academica_id"] = data.get("unidadAcademica")
            elif rol == "secretaria":
                registro["facultad_id"] = data.get("facultad")

            try:
                usuario_id = UserService.registrar(registro)
                return JsonResponse({"id": usuario_id, "message": "registro creado"}, status=201)
            except ValueError as e:
                return JsonResponse({"error": str(e)}, status=400)
        
        return JsonResponse({"error": "Método no permitido"}, status=405)
        
    def login(request):
        if request.method == "POST":
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Formato JSON inválido."}, status=400)

            email = data.get("email")
            password = data.get("password")

            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user) 
                return JsonResponse({"message": "Inicio de sesión exitoso"}, status=200)

            return JsonResponse({"error": "No se encontró ningun usuario."}, status=401)
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    @login_required()
    def logout(request):
        if request.method == "POST":
            logout(request)
            return JsonResponse({"message": "Cierre de sesión exitoso"}, status=200)
        return JsonResponse({"error": "Método no permitido"}, status=405)

    # * Método para listar organizadores
    @login_required()
    def listar_organizadores(request):
        # Check for query parameters
        if request.method == "GET":
            if request.GET:
                nombreCompletoSearch = request.GET.get("q")
                if nombreCompletoSearch:
                    organizadores = UserService.filtrar_organizadores_por_nombre_completo(nombreCompletoSearch, request.user.idUsuario)

                     # No results found
                    if not organizadores:
                        return JsonResponse({
                            "message": "No se encontraron usuarios organizadores",
                            "messageType": "info"
                        }, status=200)
                    else:
                        # Return all the organizations
                        return JsonResponse({
                            "items": organizadores,
                            "message": "Búsqueda completada correctamente!",
                            "messageType": "success"
                        }, status=200)
                else:
                    return JsonResponse({"error": "No se envió el query param adecuado"}, status=400)
            else:
                organizadores = list(UserService.listar_organizadores())
                return JsonResponse({"items": organizadores}, status=200)

        return JsonResponse({"error": "Método no permitido"}, status=405)

    @login_required()
    def obtener_por_id(request, id):
        if request.method == "GET":
            user = UserService.obtener_por_id(id)
            if not user: return JsonResponse({"error": "No se encontró ningun usuario"}, status=404)
            
            data = {
                "organizador": {  
                    "idUsuario": user["idUsuario"],
                    "numeroIdentificacion": user["numeroIdentificacion"],
                    "nombres": user["nombres"],
                    "apellidos": user["apellidos"],
                    "email": user["email"],
                    "telefono": user["telefono"],
                    "rol": user["rol"]
                }
            }
            return JsonResponse(data, status=200)
        return JsonResponse({"error": "Método no permitido"}, status=405)