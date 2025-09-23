from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from .service import UserService
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

