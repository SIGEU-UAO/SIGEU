from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from sigeu.decorators import no_superuser_required, organizador_required
from .forms.event import RegistroEventoForm
from .forms.associations.OrganizadorEvento import OrganizadorEventoForm
from .forms.associations.OrganizacionesInvitadas import OrganizacionInvitadaForm
from apps.core.forms import ModalBuscarInstalacionForm
from apps.users.forms import ModalBuscarOrganizadorForm
from apps.external_organizations.forms import RegistroForm, ModalBuscarOrganizacionForm

@no_superuser_required
@login_required()
@organizador_required
def formulario_registro(request):
    current_user = request.user
    mainForm = RegistroEventoForm()

    # Formularios de Busqueda
    modalBuscarInstalacionesForm = ModalBuscarInstalacionForm()
    modalBuscarOrganizadoresForm = ModalBuscarOrganizadorForm()
    modalBuscarOrganizacionesForm = ModalBuscarOrganizacionForm()

    # Formularios de asignacion
    modalAsociarOrganizadorForm = OrganizadorEventoForm()
    modalAsociarOrganizacionForm = OrganizacionInvitadaForm()

    # Formulario de creacion de organizacion externa
    registroOrganizacionForm = RegistroForm()

    return render(request, "events/registro_evento.html", {
        "header_title": "Registrar Evento Universitario", 
        "header_paragraph": "Administra las entidades que participan en tus eventosOrganiza y lleva el control de todos tus eventos en un solo lugar",
        "form": mainForm,
        "modal_buscar_instalaciones_form": modalBuscarInstalacionesForm,
        "modal_buscar_organizadores_form": modalBuscarOrganizadoresForm,
        "modal_buscar_organizaciones_form": modalBuscarOrganizacionesForm,
        "modal_asociar_organizador_form": modalAsociarOrganizadorForm,
        "modal_asociar_organizacion_form": modalAsociarOrganizacionForm,
        "registro_organizacion_form": registroOrganizacionForm,
        "current_user_data": { "id": current_user.idUsuario, "nombreCompleto": f"{current_user.nombres} {current_user.apellidos}", "rol": current_user.rol },
        "active_page": "registrar-evento"
    })

@no_superuser_required
@login_required()
@organizador_required
def mis_eventos(request):
    # * Aqui deberias de cargar los eventos del usuario actual 

    return render(request, "events/mis_eventos.html", {
        "header_title": "Mis Eventos", 
        "header_paragraph": "Administra y lleva el control de todos tus eventos en un solo lugar de manera fácil y eficiente.",
        # Aquí deberias de pasar los eventos del usuario actual
        "active_page": "registrar-evento"
    })