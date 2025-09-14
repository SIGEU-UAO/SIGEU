from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from .forms import RegistroForm, InicioSesionForm
from .services.RegistroService import RegistroService
from .services.InicioSesionService import InicioSesionService
from django.http import HttpResponseRedirect


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
    if request.method == "GET":
        form = InicioSesionForm()
        return render(request, "authentication/inicio_sesion.html", {"form": form})

    if request.method == "POST":
        form = InicioSesionForm(request.POST)
        if not form.is_valid():
            errors = {field: list(errs) for field, errs in form.errors.items()}
            return JsonResponse({"error": "invalid_form", "errors": errors}, status=400)

        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]

        result = InicioSesionService.iniciar(request, email, password)

        if not result.get("ok"):
            # [ADICIÓN] devolver JSON con el error para que el front (notyf) lo muestre
            code = result.get("error")
            if code == "missing_fields":
                return JsonResponse({"error": "Faltan el correo y/o la contraseña."}, status=400)
            if code == "invalid_credentials":
                return JsonResponse({"error": "Correo o contraseña incorrectos."}, status=401)
            if code == "inactive_account":
                return JsonResponse({"error": "Tu cuenta está inactiva. Contacta al administrador."}, status=403)
            return JsonResponse({"error": "Error desconocido al iniciar sesión."}, status=400)

       
        request.session["usuario_id"] = result["user_id"]                  
        request.session["rol"] = (request.user.groups.first().name if request.user.groups.exists() else "Sin grupo")  # [ADICIÓN]
        request.session["nombre"] = f"{getattr(request.user, 'nombres', '')} {getattr(request.user, 'apellidos', '')}".strip()  # [ADICIÓN]

        # Devolver JSON de éxito para que el front haga el redirect y muestre notyf
        return JsonResponse({"message": "Inicio de sesión exitoso", "id": result["user_id"]}, status=200)

    return JsonResponse({"error": "Método no permitido."}, status=405)


class InicioSesionView(View):
    template_name = "authentication/inicio_sesion.html"

    def get(self, request):
        return render(request, self.template_name, {"form": InicioSesionForm()})

    def post(self, request):
        form = InicioSesionForm(request.POST)
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]

        result = InicioSesionService.iniciar(request, email, password)
        if not result.get("ok"):
            code = result.get("error")
            if code == "missing_fields":
                return JsonResponse({"error": "Faltan el correo y/o la contraseña."}, status=400)
            if code == "invalid_credentials":
                return JsonResponse({"error": "Correo o contraseña incorrectos."}, status=401)
            if code == "inactive_account":
                return JsonResponse({"error": "Tu cuenta está inactiva. Contacta al administrador."}, status=403)
            return JsonResponse({"error": "Error desconocido al iniciar sesión."}, status=400)

        request.session["usuario_id"] = result["user_id"]
        request.session["rol"] = (request.user.groups.first().name if request.user.groups.exists() else "Sin grupo")
        request.session["nombre"] = f"{getattr(request.user, 'nombres', '')} {getattr(request.user, 'apellidos', '')}".strip()

        return JsonResponse({"message": "Inicio de sesión exitoso", "id": result["user_id"]}, status=200)