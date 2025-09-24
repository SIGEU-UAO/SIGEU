from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.external_organizations.forms import RegistroForm
from apps.external_organizations.service import OrganizacionExternaService
from sigeu.decorators import no_superuser_required, organizador_required

@no_superuser_required
@login_required()
@organizador_required
def formulario_registro(request):
    form = RegistroForm()
    return render(request, "external_organizations/registro_organizacion.html", {
        "header_title": "Registrar Organización Externa",
        "header_paragraph": "Administra las entidades que participan en tus eventos",
        "form": form,
        "active_page": "registrar-org"
    })

@no_superuser_required
@login_required()
@organizador_required
def listado(request):
    return render(request, "external_organizations/listado_organizaciones.html", {
        "header_title": "Lista de Organizaciones Externas",
        "header_paragraph": "Consulta, administra y gestiona tus organizaciones externas en un solo lugar",
        "active_page": "listar-org"
    })