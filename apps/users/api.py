from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from .service import UserService, validate_new_password, save_password_history
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

    def perfil(request):
        # Actualización de perfil vía API (POST JSON)
        if request.method == "POST":
            if not request.user.is_authenticated:
                return JsonResponse({"error": "No autenticado"}, status=401)
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Formato JSON inválido."}, status=400)

            # Asegurar que los campos deshabilitados/requeridos estén incluidos
            post_data = dict(data) if isinstance(data, dict) else {}
            for fld in ["numeroIdentificacion", "nombres", "apellidos", "email", "telefono"]:
                if not post_data.get(fld):
                    post_data[fld] = getattr(request.user, fld, "")
            # Incluir codigo_estudiante si el usuario es estudiante y no viene
            if "codigo_estudiante" not in post_data and hasattr(request.user, 'estudiante'):
                post_data["codigo_estudiante"] = getattr(getattr(request.user, 'estudiante', None), 'codigo_estudiante', "")

            # Validar con el mismo formulario usado en la vista
            from .forms import EditarPerfil
            form = EditarPerfil(post_data, user=request.user)
            if not form.is_valid():
                return JsonResponse({"error": form.errors}, status=400)

            cd = form.cleaned_data
            # Actualizar datos básicos
            request.user.nombres = cd["nombres"]
            request.user.apellidos = cd["apellidos"]
            request.user.telefono = cd["telefono"]

            # Actualizar código de estudiante si aplica
            if "codigo_estudiante" in cd and hasattr(request.user, 'estudiante'):
                request.user.estudiante.codigo_estudiante = cd["codigo_estudiante"]
                request.user.estudiante.save()

            # Cambio de contraseña con validación de historial (opcional)
            if cd.get("contraseña"):
                try:
                    UserService.cambiar_password(request.user, cd["contraseña"])
                except ValueError as e:
                    return JsonResponse({"error": {"contraseña": [str(e)]}}, status=400)
            else:
                request.user.save()

            # Respuesta
            codigo_estudiante = ""
            if hasattr(request.user, 'estudiante'):
                codigo_estudiante = request.user.estudiante.codigo_estudiante

            return JsonResponse({
                "success": True,
                "nombres": request.user.nombres,
                "apellidos": request.user.apellidos,
                "telefono": request.user.telefono,
                "codigo_estudiante": codigo_estudiante
            }, status=200)

        return JsonResponse({"error": "Método no permitido"}, status=405)

