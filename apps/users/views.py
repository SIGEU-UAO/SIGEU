from pyexpat.errors import messages
from django.http import JsonResponse
from django.shortcuts import render ,redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import RegistroForm, InicioSesionForm, EditarPerfil
from django.contrib.auth.decorators import login_required
from sigeu.decorators import no_superuser_required
from .service import UserService, validate_new_password, save_password_history

import json

# Solo permite acceso a usuarios que NO sean superuser
def not_superuser(user):
    return not user.is_superuser

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
        # Obtener código de estudiante si el usuario es estudiante
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
        form = EditarPerfil(initial=initial_data, user=request.user)
        return render(request, "users/editar_perfil.html", {"form": form, "active_page": "perfil"})

    elif request.method == "POST":
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
        
        # Manejar datos de formulario (AJAX o normal)
        if request.POST:
            post_data = request.POST.copy()
        elif is_ajax and request.content_type == 'application/json':
            try:
                json_data = json.loads(request.body)
                post_data = {}
                for key, value in json_data.items():
                    post_data[key] = value
            except json.JSONDecodeError:
                return JsonResponse({"success": False, "errors": {"json": ["Formato JSON inválido"]}}, status=400)
        else:
            post_data = {}
            
        # Asegurar que los campos deshabilitados/requeridos estén incluidos
        for fld in ["numeroIdentificacion", "nombres", "apellidos", "email", "telefono"]:
            if not post_data.get(fld):
                post_data[fld] = getattr(request.user, fld, "")

        form = EditarPerfil(post_data, user=request.user)

        if form.is_valid():
            cd = form.cleaned_data
            request.user.nombres = cd["nombres"]
            request.user.apellidos = cd["apellidos"]
            request.user.telefono = cd["telefono"]
            
            # Actualizar código de estudiante si existe y el usuario es estudiante
            if "codigo_estudiante" in cd and hasattr(request.user, 'estudiante'):
                request.user.estudiante.codigo_estudiante = cd["codigo_estudiante"]
                request.user.estudiante.save()
            
            # Cambio de contraseña con validación de historial
            if cd.get("contraseña"):
                            try:
                                from .service import validate_new_password, save_password_history
                                validate_new_password(request.user, cd["contraseña"])
                                request.user.set_password(cd["contraseña"])
                                request.user.save()
                                save_password_history(request.user)
                            except ValueError as e:
                                if is_ajax:
                                    return JsonResponse({"success": False, "errors": {"contraseña": [str(e)]}}, status=400)
                                form.add_error("contraseña", str(e))
                                return render(request, "users/editar_perfil.html", {"form": form, "active_page": "perfil"})
            else:
                request.user.save()
            # If the request is an AJAX/fetch call, return JSON with updated fields
            if is_ajax:
                # Obtener código de estudiante actualizado
                codigo_estudiante = ""
                if hasattr(request.user, 'estudiante'):
                    codigo_estudiante = request.user.estudiante.codigo_estudiante
                
                return JsonResponse({
                    "success": True,
                    "nombres": request.user.nombres,
                    "apellidos": request.user.apellidos,
                    "telefono": request.user.telefono,
                    "codigo_estudiante": codigo_estudiante
                })
            return redirect("perfil")

        # If form is invalid and it's an AJAX request, return JSON errors (avoid returning full HTML)
        if is_ajax:
            # Include received values for debugging
            received = {fld: post_data.get(fld) for fld in ["numeroIdentificacion", "nombres", "apellidos", "email", "telefono", "contraseña"]}
            return JsonResponse({"success": False, "errors": form.errors, "received": received}, status=400)

        return render(request, "users/editar_perfil.html", {"form": form, "active_page": "perfil"})

    return JsonResponse({"error": "Método no permitido"}, status=405)
 
@login_required
def change_password(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Formato JSON inválido."}, status=400)

    new_password = data.get("new_password")
    if not new_password:
        return JsonResponse({"error": "La nueva contraseña es requerida"}, status=400)

    try:
        UserService.cambiar_password(request.user, new_password)
        return JsonResponse({"success": "Contraseña actualizada con éxito"}, status=200)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)