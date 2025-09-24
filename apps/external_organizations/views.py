from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.external_organizations.forms import RegistroForm
from sigeu.decorators import no_superuser_required


@no_superuser_required
@login_required()
def formulario_registro(request):
    form = RegistroForm()
    return render(request, "external_organizations/registro_organizacion.html", {
        "header_title": "Registrar Organización Externa",
        "header_paragraph": "Administra las entidades que participan en tus eventos",
        "form": form,
        "active_page": "registrar-org"
    })

