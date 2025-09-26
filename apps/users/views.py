from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import RegistroForm, InicioSesionForm, EditarPerfil
from django.contrib.auth.decorators import login_required
from sigeu.decorators import no_superuser_required
import json
from .service import UserService       
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
        form = EditarPerfil(request.POST, user=request.user)
        if form.is_valid():
            try:
                # Actualizar los campos editables del usuario
                user = request.user
                
                # Actualizar teléfono si cambió
                if form.cleaned_data['telefono'] != user.telefono:
                    user.telefono = form.cleaned_data['telefono']
                
                # Actualizar contraseña si se proporcionó una nueva
                nueva_contraseña = form.cleaned_data.get('contraseña')
                if nueva_contraseña:
                    UserService.cambiar_password(user, nueva_contraseña)
                
                # Actualizar código de estudiante si el usuario es estudiante
                if hasattr(user, 'estudiante') and 'codigo_estudiante' in form.cleaned_data:
                    codigo_estudiante = form.cleaned_data['codigo_estudiante']
                    if codigo_estudiante and codigo_estudiante != user.estudiante.codigo_estudiante:
                        user.estudiante.codigo_estudiante = codigo_estudiante
                        user.estudiante.save()
                
                user.save()
                
                # Mensaje de éxito - podrías usar Django messages framework aquí
                return render(request, "users/editar_perfil.html", {
                    "form": form, 
                    "active_page": "perfil",
                    "success_message": "Perfil actualizado correctamente"
                })
                
            except Exception as e:
                return render(request, "users/editar_perfil.html", {
                    "form": form, 
                    "active_page": "perfil",
                    "error_message": f"Error al actualizar el perfil: {str(e)}"
                })
        else:
            # Form is not valid, return with errors
            return render(request, "users/editar_perfil.html", {
                "form": form, 
                "active_page": "perfil",
                "error_message": "Por favor corrige los errores en el formulario"
            })
    
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