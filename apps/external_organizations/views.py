from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from apps.external_organizations.forms import RegistroForm
from sigeu.decorators import no_superuser_required

@no_superuser_required
@login_required()
def formulario_registro(request):
    if request.method == "GET":
        form = RegistroForm()
        return render(request, "external_organizations/registro_organizacion.html", {
            "header_title": "Registrar Organización Externa", 
            "header_paragraph": "Administra las entidades que participan en tus eventos",
            "form": form,
            "active_page": "registrar-org"
        })
    elif request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            try:
                from .service import OrganizacionExternaService
                org_id = OrganizacionExternaService.registrar(form.cleaned_data)
                # Redirect to orgs register page on success
                return HttpResponseRedirect(reverse('registrar_org')) 
            except ValueError as e:
                # If there's an error, re-render the form with error message
                return render(request, "external_organizations/registro_organizacion.html", {
                    "header_title": "Registrar Organización Externa", 
                    "header_paragraph": "Administra las entidades que participan en tus eventos",
                    "form": form,
                    "active_page": "registrar-org",
                    "error_message": str(e)
                })
        else:
            # If form is not valid, re-render with errors
            return render(request, "external_organizations/registro_organizacion.html", {
                "header_title": "Registrar Organización Externa", 
                "header_paragraph": "Administra las entidades que participan en tus eventos",
                "form": form,
                "active_page": "registrar-org"
            })
    return JsonResponse({"error": "Método no permitido"}, status=405)
