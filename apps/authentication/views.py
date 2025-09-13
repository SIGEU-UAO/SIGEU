from django.http import JsonResponse
from django.shortcuts import render
from .forms import RegistroForm, InicioSesionForm
from .services.RegistroService import RegistroService
from .services.InicioSesionService import InicioSesionService
from django.db import IntegrityError

def _mensaje_integridad(e: Exception) -> str:
    s = str(e).lower()
    if "numeroidentificacion" in s:
        return "El documento de identidad ya está registrado."
    if "email" in s:
        return "El correo electrónico ya está registrado."
    if "codigo_estudiante" in s:
        return "Ese código de estudiante ya existe."
    return "Datos duplicados: ya existe un registro con esos valores."

def formulario_registro(request):

    if request.method == "GET":
        form = RegistroForm()
        return render(request, "authentication/registro.html", {"form": form})

    if request.method == "POST":
        rol = request.POST.get("rol")

        registro = {
            "email": request.POST.get("email"),
            "password": request.POST.get("password1"),
            "nombres": request.POST.get("nombre"),
            "apellidos": request.POST.get("apellido"),
            "telefono": request.POST.get("telefono"),
            "numeroIdentificacion": request.POST.get("documento"),
            "rol": rol,
        }

        if rol == "estudiante":
            registro["codigo_estudiante"] = request.POST.get("codigo_estudiante")
            registro["programa_id"] = request.POST.get("programa")
        elif rol == "docente":
            registro["unidad_academica_id"] = request.POST.get("unidadAcademica")
        elif rol == "secretaria":
            registro["facultad_id"] = request.POST.get("facultad")

        try:
            usuario_id = RegistroService.registrar(registro)
            return JsonResponse({"id": usuario_id, "message": "registro creado"}, status=201)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "método no permitido"}, status=405)


def inicio_sesion(request):
    # GET -> muestra el formulario HTML correcto
    if request.method == "GET":
        form = InicioSesionForm()
        return render(request, "authentication/inicio_sesion.html", {"form": form})
 
    # POST -> ejemplo simple usando el service
    if request.method == "POST":
        form = InicioSesionForm(request.POST)
        if not form.is_valid():
            # re-render con errores del form
            return render(request, "authentication/inicio_sesion.html", {"form": form}, status=400)

        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]

        ok, user_id = InicioSesionService.autenticar(email, password)
        if ok:
            return JsonResponse({"message": "login ok", "id": user_id})
        return JsonResponse({"error": "credenciales inválidas"}, status=401)

    return JsonResponse({"error": "método no permitido"}, status=405)