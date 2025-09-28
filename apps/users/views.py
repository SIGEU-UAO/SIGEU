from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import RegistroForm, InicioSesionForm, EditarPerfilForm
from django.contrib.auth.decorators import login_required
from sigeu.decorators import no_superuser_required
from .service import UserService
import json
import logging

logger = logging.getLogger(__name__)

def formulario_registro(request):
    if request.method == "GET":
        form = RegistroForm()
        return render(request, "users/registro.html", {"form": form, "password_icons": ["ri-eye-fill", "ri-information-2-fill" ]})
    return JsonResponse({"error": "Método no permitido"}, status=405)


def inicio_sesion(request):
    # If already authenticated, redirect to the dashboard
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("dashboard"))

    if request.method == "GET":
        form = InicioSesionForm()
        return render(request, "users/inicio_sesion.html", {"form": form, "password_icons": ["ri-eye-fill"]})
    return JsonResponse({"error": "Método no permitido"}, status=405)

@no_superuser_required
@login_required()
def dashboard(request):
    if request.method == "GET":
        return render(request, "users/dashboard.html", {
            "header_title": f"Hola, {request.user.nombres} {request.user.apellidos} 👋", 
            "header_paragraph": "Bienvenido de vuelta a SIGEU",
            "active_page": "dashboard"
        })
    return JsonResponse({"error": "Método no permitido"}, status=405)

@no_superuser_required
@login_required()
def editar_perfil(request):
    if request.method == "GET":
        # Get student code if user is student
        codigo_estudiante = ""
        if hasattr(request.user, 'estudiante'):
            codigo_estudiante = request.user.estudiante.codigo_estudiante
        
        initial_data = {
            "numeroIdentificacion": request.user.numeroIdentificacion,
            "nombres": request.user.nombres,
            "apellidos": request.user.apellidos,
            "email": request.user.email,
            "telefono": request.user.telefono,
            "contraseña": "",   
            "codigo_estudiante": codigo_estudiante
        }
        form = EditarPerfilForm(initial=initial_data, user=request.user)
        return render(request, "users/editar_perfil.html", {"form": form, "active_page": "perfil"})
    
    elif request.method == "POST":
        # Basic request logs (non-sensitive)
        logger.info("POST /perfil/ recibido. Content-Type=%s", request.content_type)
        
        # Handle profile update via AJAX
        if not request.user.is_authenticated:
            return JsonResponse({"error": "No autenticado"}, status=401)
        
        try:
            data = json.loads(request.body)
            logger.debug("Datos parseados: %s", data)
        except json.JSONDecodeError as e:
            logger.warning("Formato JSON inválido: %s", e)
            return JsonResponse({"error": "Formato JSON inválido."}, status=400)

        # Ensure that disabled/required fields are included
        post_data = dict(data) if isinstance(data, dict) else {}
        for fld in ["numeroIdentificacion", "nombres", "apellidos", "email", "telefono"]:
            if not post_data.get(fld):
                post_data[fld] = getattr(request.user, fld, "")
        
        # Include codigo_estudiante if user is student and not provided
        if "codigo_estudiante" not in post_data and hasattr(request.user, 'estudiante'):
            post_data["codigo_estudiante"] = getattr(getattr(request.user, 'estudiante', None), 'codigo_estudiante', "")

        logger.debug("Datos finales para validación: %s", post_data)

        # Validate with the same form used in the view
        form = EditarPerfilForm(post_data, user=request.user)
        if not form.is_valid():
            # Log detallado de errores
            try:
                errors_json = form.errors.as_json()
            except Exception:
                errors_json = str(form.errors)
            logger.warning("Errores de validación en perfil: %s", errors_json)
            return JsonResponse({"error": form.errors, "message": "Por favor corrige los errores en el formulario"}, status=400)

        cd = form.cleaned_data
        logger.debug("Datos validados: %s", cd)
        
        # Update basic data
        request.user.nombres = cd["nombres"]
        request.user.apellidos = cd["apellidos"]
        request.user.telefono = cd["telefono"]

        # Update student code if applicable
        if "codigo_estudiante" in cd and hasattr(request.user, 'estudiante'):
            request.user.estudiante.codigo_estudiante = cd["codigo_estudiante"]
            request.user.estudiante.save()

        # Password change with history validation (optional)
        if cd.get("contraseña"):
            try:
                UserService.cambiar_password(request.user, cd["contraseña"])
            except ValueError as e:
                logger.info("Validación de contraseña fallida: %s", e)
                return JsonResponse({"error": {"contraseña": [str(e)]}}, status=400)
        else:
            request.user.save()

        # Response
        codigo_estudiante = ""
        if hasattr(request.user, 'estudiante'):
            codigo_estudiante = request.user.estudiante.codigo_estudiante

        logger.info("Perfil actualizado correctamente para usuario %s", request.user.email)
        return JsonResponse({
            "success": True,
            "nombres": request.user.nombres,
            "apellidos": request.user.apellidos,
            "telefono": request.user.telefono,
            "codigo_estudiante": codigo_estudiante
        }, status=200)
    
    return JsonResponse({"error": "Método no permitido"}, status=405)