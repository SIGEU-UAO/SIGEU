from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from .service import UserService
from django.contrib.auth.decorators import login_required
from .forms import EditarPerfilForm
from django.db import IntegrityError
import json
import re

class UsersAPI():
    def registro(request):
        if request.method == "POST":
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Formato JSON inválido"}, status=400)

            # Validate if the email ends with @uao.edu.co
            email = data.get("email", "")
            if not email.endswith("@uao.edu.co"):
                return JsonResponse({"error": "El correo electrónico debe pertenecer al dominio @uao.edu.co"}, status=400)
            
            # Validate that the identification number has between 8 and 10 characters and the phone number has 10 characters.
            identificacion = data.get("documento", "")
            telefono = data.get("telefono", "")
            if not (8 <= len(identificacion) <= 10):
                return JsonResponse({"error": "El número de identificación debe tener entre 8 y 10 caracteres"}, status=400)
            if len(telefono) != 10:
                return JsonResponse({"error": "El número de teléfono debe tener exactamente 10 caracteres"}, status=400)
            
            # Validate the password with the regex
            setting_password = data.get("password1", "")
            password_pattern = re.compile(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$')
            if not password_pattern.match(setting_password):
                return JsonResponse({"error": "La contraseña debe tener al menos 8 caracteres, incluyendo una letra mayúscula, una letra minúscula, un número y opcionalmente un carácter especial."}, status=400)

            rol = data.get("rol")

            registro = {
                "email": email,
                "password": setting_password,
                "nombres": data.get("nombre"),
                "apellidos": data.get("apellido"),
                "telefono": telefono,
                "numeroIdentificacion": identificacion,
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
                return JsonResponse({"id": usuario_id, "message": f"{rol.capitalize()} creado/a correctamente"}, status=201)
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

            user = UserService.obtener_usuario_por_email(email)
            if not user:
                return JsonResponse({"error": "No se encontró ningun usuario."}, status=401)
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user) 
                return JsonResponse({"message": "Inicio de sesión exitoso"}, status=200)
            else:
                return JsonResponse({"error": "Contraseña incorrecta"}, status=401)
            
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    @login_required
    def logout(request):
        if request.method == "POST":
            logout(request)
            return JsonResponse({"message": "Cierre de sesión exitoso"}, status=200)
        return JsonResponse({"error": "Método no permitido"}, status=405)
        
    @login_required
    def editar_perfil(request):
        # Profile update via API (PUT JSON)
        if request.method == "PUT":
            if not request.user.is_authenticated:
                return JsonResponse({"error": "No autenticado"}, status=401)
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({"error": "formato JSON inválido."}, status=400)

            # Ensure that disabled/required fields are included
            put_data = dict(data) if isinstance(data, dict) else {}
            for fld in ["numeroIdentificacion", "nombres", "apellidos", "email", "telefono"]:
                if not put_data.get(fld):
                    put_data[fld] = getattr(request.user, fld, "")
        
            # Validate with the same form used in the view
            
            form = EditarPerfilForm(put_data, user=request.user)
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
                except ValueError:
                    return JsonResponse({"error": "La nueva contraseña no puede ser igual a las anteriores. Intenta con una diferente."}, status=400)
                except IntegrityError as e:
                    msg = str(e).lower()
                    if "telefono" in msg:
                        return JsonResponse({"error": "No puedes registrar un teléfono ya asociado"}, status=400)
                    return JsonResponse({"error": "Violación de unicidad al actualizar el perfil."}, status=400)
            else:
                # Save and rely on DB unique constraints
                try:
                    request.user.save()
                except IntegrityError as e:
                    msg = str(e).lower()
                    if "telefono" in msg:
                        return JsonResponse({"error": "No puedes registrar un teléfono ya asociado"}, status=400)
                    return JsonResponse({"error": "Violación de unicidad al actualizar el perfil."}, status=400)

            # Response
            return JsonResponse({
                "success": True,
                "nombres": request.user.nombres,
                "apellidos": request.user.apellidos,
                "telefono": request.user.telefono,
            }, status=200)

        return JsonResponse({"error": "Metodo no permitido"}, status=405)

    # * Método para listar organizadores
    @login_required
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

    @login_required
    def obtener_organizador_por_id(request, id):
        if request.method == "GET":
            user = UserService.obtener_organizador_por_id(id)
            if not user: return JsonResponse({"error": "No se encontró ningun organizador con dicha ID"}, status=404)
            
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