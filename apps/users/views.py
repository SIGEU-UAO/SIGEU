from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import RegistroForm, InicioSesionForm
from django.contrib.auth.decorators import login_required
from sigeu.decorators import no_superuser_required

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