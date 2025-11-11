from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from apps.external_organizations.forms import RegistroForm
from apps.external_organizations.service import OrganizacionExternaService
from apps.events.services.event import EventoService
from sigeu.decorators import no_superuser_required, organizador_required

@no_superuser_required
@login_required()
@organizador_required
def listado(request):
    notificaciones = EventoService.obtener_notificaciones(request.user)

    return render(request, "external_organizations/listado_organizaciones.html", {
        "header_title": "Lista de Organizaciones Externas",
        "header_paragraph": "Consulta, administra y gestiona tus organizaciones externas en un solo lugar",
        "active_page": "listar-org",
        "notificaciones": notificaciones,
    })    

@no_superuser_required
@login_required()
@organizador_required
def editar(request, pk):
    org = OrganizacionExternaService.obtener_por_id(pk)
    if not org:
        return redirect("not_found")
    elif not OrganizacionExternaService.es_creador(request.user, pk):
        return redirect("forbidden")
    
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
    notificaciones = EventoService.obtener_notificaciones(request.user)

    return render(request, "external_organizations/editar_organizacion.html", {
        "header_title": "Editar Organización Externa",
        "header_paragraph": "Modifica los datos de la organización externa seleccionada",
        "form": form,
        "active_page": "listar-org",
        "pk": pk,
        "notificaciones": notificaciones,
    })