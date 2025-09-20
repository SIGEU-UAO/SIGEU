from django.http import JsonResponse
from django.shortcuts import render ,redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import RegistroForm, InicioSesionForm, EditarPerfil
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

@no_superuser_required
@login_required()
def editar_perfil(request):
    if request.method == "GET":
        initial_data = {
            "numeroIdentificacion": request.user.numeroIdentificacion,
            "nombres": request.user.nombres,
            "apellidos": request.user.apellidos,
            "email": request.user.email,
            "telefono": request.user.telefono,
            "contraseña": "",   
            "codigo_estudiante": getattr(request.user, "codigo_estudiante", "")
        }
        form = EditarPerfil(initial=initial_data, user=request.user)
        return render(request, "users/editar_perfil.html", {"form": form, "active_page": "perfil"})

    elif request.method == "POST":
        # Copy POST and ensure disabled/required fields are included (browsers omit disabled inputs)
        post_data = request.POST.copy()
        for fld in ["numeroIdentificacion", "nombres", "apellidos", "email", "telefono"]:
            if not post_data.get(fld):
                post_data[fld] = getattr(request.user, fld, "")

        form = EditarPerfil(post_data, user=request.user)
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

        if form.is_valid():
            cd = form.cleaned_data
            request.user.nombres = cd["nombres"]
            request.user.apellidos = cd["apellidos"]
            request.user.telefono = cd["telefono"]
            if "codigo_estudiante" in cd:
                request.user.codigo_estudiante = cd["codigo_estudiante"]
            if cd.get("contraseña"):
                request.user.set_password(cd["contraseña"])
            request.user.save()
            # If the request is an AJAX/fetch call, return JSON with updated fields
            if is_ajax:
                return JsonResponse({
                    "success": True,
                    "nombres": request.user.nombres,
                    "apellidos": request.user.apellidos,
                    "telefono": request.user.telefono,
                    "codigo_estudiante": getattr(request.user, "codigo_estudiante", "")
                })
            return redirect("perfil")

        # If form is invalid and it's an AJAX request, return JSON errors (avoid returning full HTML)
        if is_ajax:
            # Include received values for debugging
            received = {fld: post_data.get(fld) for fld in ["numeroIdentificacion", "nombres", "apellidos", "email", "telefono", "contraseña"]}
            return JsonResponse({"success": False, "errors": form.errors, "received": received}, status=400)

        return render(request, "users/editar_perfil.html", {"form": form, "active_page": "perfil"})

    return JsonResponse({"error": "Método no permitido"}, status=405)
