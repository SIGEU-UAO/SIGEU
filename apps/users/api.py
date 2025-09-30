from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from .service import UserService
from django.contrib.auth.decorators import login_required
from sigeu.decorators import no_superuser_required
from .forms import EditarPerfilForm
from .models import Usuario
from django.db import IntegrityError
import json

class UsersAPI():
    def registro(request):
        if request.method == "POST":
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Formato JSON inválido"}, status=400)

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
                return JsonResponse({"error": "formato JSON inválido"}, status=400)

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
    
    
    @login_required()
    @no_superuser_required
    def editar_perfil(request):
        # Profile update via API (POST JSON)
        if request.method == "POST":
            if not request.user.is_authenticated:
                return JsonResponse({"error": "No autenticado"}, status=401)
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({"error": "formato JSON inválido."}, status=400)

            # Ensure that disabled/required fields are included
            post_data = dict(data) if isinstance(data, dict) else {}
            for fld in ["numeroIdentificacion", "nombres", "apellidos", "email", "telefono"]:
                if not post_data.get(fld):
                    post_data[fld] = getattr(request.user, fld, "")
        
        
            # Validate with the same form used in the view
            
            form = EditarPerfilForm(post_data, user=request.user)
            if not form.is_valid():
                return JsonResponse({"error": form.errors}, status=400)

            cd = form.cleaned_data

            new_phone = cd["telefono"]

            # Update basic data
            request.user.nombres = cd["nombres"]
            request.user.apellidos = cd["apellidos"]
            request.user.telefono = new_phone

            # Password change with history validation (optional)
            if cd.get("contraseña"):
                try:
                    UserService.cambiar_password(request.user, cd["contraseña"])
                except ValueError as e:
                    return JsonResponse({"error": {"contraseña": [str(e)]}}, status=400)
                except IntegrityError:
                    return JsonResponse({"error": "Violación de unicidad al actualizar el perfil."}, status=400)
            else:
                # Save and rely on DB unique constraints
                try:
                    request.user.save()
                except IntegrityError:
                    return JsonResponse({"error": "Violación de unicidad al actualizar el perfil."}, status=400)

            # Response
            return JsonResponse({
                "success": True,
                "nombres": request.user.nombres,
                "apellidos": request.user.apellidos,
                "telefono": request.user.telefono,
            }, status=200)

        return JsonResponse({"error": "Metodo no permitido"}, status=405)

