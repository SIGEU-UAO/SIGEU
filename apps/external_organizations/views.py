from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from apps.external_organizations.forms import RegistroForm
from apps.external_organizations.service import OrganizacionExternaService
from apps.external_organizations.models import OrganizacionExterna
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

@no_superuser_required
@login_required()
@organizador_required
def editar(request, pk):
    try:
        org = OrganizacionExterna.objects.get(idOrganizacion=pk)
    except OrganizacionExterna.DoesNotExist:
        return redirect("org_no_encontrada")

    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            try:
                OrganizacionExternaService.actualizar(pk, form.cleaned_data)
                return JsonResponse({
                    "status": "success",
                    "message": "Organización actualizada correctamente."
                }, status=200)
            except ValueError as e:
                return JsonResponse({
                    "status": "error",
                    "message": str(e)
                }, status=400)
        else:
            return JsonResponse({
                "status": "error",
                "message": "Hay errores en el formulario.",
                "errors": form.errors
            }, status=400)

    # GET → renderizar el form con datos iniciales
    initial_data = {
        "nit": org.nit,
        "nombre": org.nombre,
        "representante_legal": org.representanteLegal,
        "telefono": org.telefono,
        "ubicacion": org.ubicacion,
        "sector_economico": org.sectorEconomico,
        "actividad_principal": org.actividadPrincipal,
    }
    form = RegistroForm(initial=initial_data)

    return render(request, "external_organizations/editar_organizacion.html", {
        "header_title": "Editar Organización Externa",
        "header_paragraph": "Modifica los datos de la organización externa seleccionada",
        "form": form,
        "active_page": "listar-org",
        "pk": pk,
    })


@no_superuser_required
@login_required()
@organizador_required
def org_no_encontrada(request):
    return render(request, "external_organizations/organizacion_no_encontrada.html", {
        "header_title": "Organización no encontrada",
        "header_paragraph": "La organización solicitada no existe o ha sido eliminada.",
        "active_page": "listar-org"
    })