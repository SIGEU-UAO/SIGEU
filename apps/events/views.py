from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from sigeu.decorators import no_superuser_required, organizador_required
from .forms.event import RegistroEventoForm
from apps.core.forms import ModalBuscarInstalacionForm

@no_superuser_required
@login_required()
@organizador_required
def formulario_registro(request):
    mainForm = RegistroEventoForm()
    modalBuscarInstalacionesForm = ModalBuscarInstalacionForm();
    return render(request, "events/registro_evento.html", {
        "header_title": "Registrar Evento Universitario", 
        "header_paragraph": "Administra las entidades que participan en tus eventosOrganiza y lleva el control de todos tus eventos en un solo lugar",
        "form": mainForm,
        "modal_buscar_instalaciones_form": modalBuscarInstalacionesForm,
        "active_page": "registrar-evento"
    })