from django.http import JsonResponse
from django.shortcuts import render
from .forms import RegistroForm
from .services.RegistroService import RegistroService

def formulario_registro(request):
    # - GET: I render the HTML form so we can open it directly in the browser.
    # - POST: I return JSON and delegate the creation logic to the service layer.
    # If at some point we want this endpoint to be JSON-only (as in the doc), we can
    # just remove the GET block below and keep POST + the 405 at the end.

    if request.method == "GET":
        # : I instantiate the form only to feed the template with fields/choices.
        # The server-side validation still lives in the form if we ever call form.is_valid().
        form = RegistroForm()
        return render(request, "authentication/registro.html", {"form": form})

    if request.method == "POST":
        # : I map incoming form field names to the keys the service expects.
        # I intentionally keep the mapping explicit to make it easy to maintain if the form changes.
        rol = request.POST.get("rol")

        registro = {
            # : The manager behind Usuario.objects.create_user will hash the password.
            "email": request.POST.get("email"),
            "password": request.POST.get("password1"),
            "nombres": request.POST.get("nombre"),
            "apellidos": request.POST.get("apellido"),
            "telefono": request.POST.get("telefono"),
            "numeroIdentificacion": request.POST.get("documento"),
            "rol": rol,
        }

        # : Role-specific fields — I only attach what the service needs for each role.
        if rol == "estudiante":
            registro["codigo_estudiante"] = request.POST.get("codigo_estudiante")
            registro["programa_id"] = request.POST.get("programa")
        elif rol == "docente":
            registro["unidad_academica_id"] = request.POST.get("unidadAcademica")
        elif rol == "secretaria":
            registro["facultad_id"] = request.POST.get("facultad")

        #: I delegate to the service. The service encapsulates all business decisions
        # (create Usuario + role entity). If the service raises, we can wrap this in try/except
        # and return a 400; I'm keeping it minimal for now because that's what we agreed on.
        usuario_id = RegistroService.registrar(registro)

        #: 201 Created because we actually created a resource (the user).
        return JsonResponse({"id": usuario_id, "message": "registro creado"}, status=201)

    # : For any other HTTP method, I return an explicit 405 to be clear about allowed verbs.
    return JsonResponse({"error": "método no permitido"}, status=405)
