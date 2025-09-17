from django.http import JsonResponse
from django.shortcuts import render
from .forms import RegistroForm, InicioSesionForm

def formulario_registro(request):
    if request.method == "GET":
        form = RegistroForm()
        return render(request, "authentication/registro.html", {"form": form, "password_icons": ["authentication/assets/icons/eye.svg", "authentication/assets/icons/info.svg" ]})
    return JsonResponse({"error": "Método no permitido"}, status=405)


def inicio_sesion(request):
    if request.method == "GET":
        form = InicioSesionForm()
        return render(request, "authentication/inicio_sesion.html", {"form": form})
    return JsonResponse({"error": "Método no permitido"}, status=405)