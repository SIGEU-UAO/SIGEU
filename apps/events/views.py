from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from sigeu.decorators import no_superuser_required, organizador_required
from .forms.event import RegistroEventoForm
from .forms.associations.coordinadorEvento import CoordinadorEventoForm
from apps.core.forms import ModalBuscarInstalacionForm
from apps.users.forms import ModalBuscarOrganizadorForm

@no_superuser_required
@login_required()
@organizador_required
def formulario_registro(request):
    mainForm = RegistroEventoForm()
    modalBuscarInstalacionesForm = ModalBuscarInstalacionForm()
    modalBuscarOrganizadoresForm = ModalBuscarOrganizadorForm()
    modalAsociarOrganizadorForm = CoordinadorEventoForm();
    return render(request, "events/registro_evento.html", {
        "header_title": "Registrar Evento Universitario", 
        "header_paragraph": "Administra las entidades que participan en tus eventosOrganiza y lleva el control de todos tus eventos en un solo lugar",
        "form": mainForm,
        "modal_buscar_instalaciones_form": modalBuscarInstalacionesForm,
        "modal_buscar_organizadores_form": modalBuscarOrganizadoresForm,
        "modal_asociar_organizador_form": modalAsociarOrganizadorForm,
        "active_page": "registrar-evento"
    })