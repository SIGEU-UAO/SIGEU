from pyexpat.errors import messages
from django.http import JsonResponse
from django.shortcuts import render ,redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import RegistroForm, InicioSesionForm, EditarPerfil
from django.contrib.auth.decorators import login_required
from sigeu.decorators import no_superuser_required
from .service import UserService, validate_new_password, save_password_history
from django.db import IntegrityError

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