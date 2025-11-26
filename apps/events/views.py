from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from sigeu.decorators import no_superuser_required, organizador_required, secretaria_required
from .forms.event import RegistroEventoForm
from .forms.associations.organizador_evento import OrganizadorEventoForm
from .forms.associations.organizaciones_invitadas import OrganizacionInvitadaForm
from apps.core.forms import ModalBuscarInstalacionForm
from apps.users.forms import ModalBuscarOrganizadorForm
from apps.external_organizations.forms import RegistroForm, ModalBuscarOrganizacionForm
from .services.event import EventoService
from .forms.event import EvaluacionEventoForm
import random

@no_superuser_required
@login_required
@organizador_required
def formulario_registro(request):
    current_user = request.user
    mainForm = RegistroEventoForm()

    # Search Forms
    modalBuscarInstalacionesForm = ModalBuscarInstalacionForm()
    modalBuscarOrganizadoresForm = ModalBuscarOrganizadorForm()
    modalBuscarOrganizacionesForm = ModalBuscarOrganizacionForm()

    # Assignment forms
    modalAsociarOrganizadorForm = OrganizadorEventoForm()
    modalAsociarOrganizacionForm = OrganizacionInvitadaForm()

    # External organization creation form
    registroOrganizacionForm = RegistroForm()

    notificaciones = EventoService.obtener_notificaciones(request.user)

    return render(request, "events/registro_evento.html", {
        "page__title": "SIGEU | Registro Evento",
        "header_title": "Registrar Evento Universitario", 
        "header_paragraph": "Administra las entidades que participan en tus eventos. Organiza y lleva el control de todos tus eventos en un solo lugar",
        "form": mainForm,
        "modal_buscar_instalaciones_form": modalBuscarInstalacionesForm,
        "modal_buscar_organizadores_form": modalBuscarOrganizadoresForm,
        "modal_buscar_organizaciones_form": modalBuscarOrganizacionesForm,
        "modal_asociar_organizador_form": modalAsociarOrganizadorForm,
        "modal_asociar_organizacion_form": modalAsociarOrganizacionForm,
        "registro_organizacion_form": registroOrganizacionForm,
        "current_user_data": { "id": current_user.id_usuario, "nombreCompleto": f"{current_user.nombres} {current_user.apellidos}", "rol": current_user.rol },
        "active_page": "registrar-evento",
        "notificaciones": notificaciones,
    })

@no_superuser_required
@login_required
@organizador_required
def mis_eventos(request):
    status = request.GET.get('status', None)   # e.g. "Aprobado"
    page = request.GET.get('page', 1)
    search = request.GET.get('search', None)
    search_by = request.GET.get('search_by', None)
    search_end = request.GET.get('search_end', '')
    hay_filtros = bool(search and search_by)

    page_obj = EventoService.listar_por_organizador(request.user, status=status, page=page, per_page=12, search=search, search_by=search_by, search_end=search_end) 

    # --- paging window calculation ---
    paginator = page_obj.paginator
    current = page_obj.number
    total = paginator.num_pages

    # page window: display up to 5 pages centered on the current one
    window_size = 5
    half = window_size // 2

    start = current - half
    end = current + half

    if start < 1:
        start = 1
        end = min(window_size, total)
    if end > total:
        end = total
        start = max(1, total - window_size + 1)

    page_numbers = list(range(start, end + 1))

    # flags for first/last and ellipsis
    show_first = (1 not in page_numbers)
    show_last = (total not in page_numbers)
    first_page = 1
    last_page = total
    left_has_more = start > 2   # there is a gap between 1 and start
    right_has_more = end < total - 1

    notificaciones = EventoService.obtener_notificaciones(request.user)

    context = {
        "header_title": "Mis Eventos",
        "header_paragraph": "Administra y lleva el control de todos tus eventos en un solo lugar.",
        "active_page": "mis-eventos",
        "notificaciones": notificaciones,
        "page_obj": page_obj,
        "status": status or "",
        # data for pagination
        "page_numbers": page_numbers,
        "show_first": show_first,
        "show_last": show_last,
        "first_page": first_page,
        "last_page": last_page,
        "left_has_more": left_has_more,
        "right_has_more": right_has_more,
        # search data
        "search": search or "",
        "search_by": search_by or "",
        "search_end": search_end or "",
        "hay_filtros": hay_filtros,
    }

    return render(request, "events/mis_eventos.html", context)

@no_superuser_required
@login_required
@secretaria_required
def eventos_enviados(request):
    page = request.GET.get('page', 1)

    try:
        page = int(page)
    except (TypeError, ValueError):
        page = 1

    page_obj = EventoService.listar_eventos_enviados(page=page, per_page=12, facultad=request.user.secretaria.facultad)

    # --- cálculo de ventana de paginación ---
    paginator = page_obj.paginator
    current = page_obj.number
    total = paginator.num_pages

    # ventana de páginas: mostrar up to 5 páginas centradas en la actual
    window_size = 5
    half = window_size // 2

    start = current - half
    end = current + half

    if start < 1:
        start = 1
        end = min(window_size, total)
    if end > total:
        end = total
        start = max(1, total - window_size + 1)

    page_numbers = list(range(start, end + 1))

    # banderas para primeros/ultimos y puntos suspensivos
    show_first = (1 not in page_numbers)
    show_last = (total not in page_numbers)
    first_page = 1
    last_page = total
    left_has_more = start > 2   # hay hueco entre 1 y start
    right_has_more = end < total - 1

    notificaciones = EventoService.obtener_notificaciones(request.user)

    context = {
        "header_title": "Eventos Pendientes de Validación",
        "header_paragraph": "Gestiona la revisión de los eventos enviados a validación en tu facultad.",
        "active_page": "eventos-enviados",
        "notificaciones": notificaciones,
        "page_obj": page_obj,
        # datos para paginación
        "page_numbers": page_numbers,
        "show_first": show_first,
        "show_last": show_last,
        "first_page": first_page,
        "last_page": last_page,
        "left_has_more": left_has_more,
        "right_has_more": right_has_more,
        # formularios
        "evaluacion_form": EvaluacionEventoForm(),
    }

    return render(request, "events/eventos_enviados.html", context)

@no_superuser_required
@login_required
def eventos_publicados(request):
    page = request.GET.get('page', 1)

    try:
        page = int(page)
    except (TypeError, ValueError):
        page = 1

    page_obj = EventoService.listar_eventos_publicados(page=page, per_page=9)


    # --- cálculo de ventana de paginación ---
    paginator = page_obj.paginator
    current = page_obj.number
    total = paginator.num_pages

    # ventana de páginas: mostrar up to 5 páginas centradas en la actual
    window_size = 5
    half = window_size // 2

    start = current - half
    end = current + half

    if start < 1:
        start = 1
        end = min(window_size, total)
    if end > total:
        end = total
        start = max(1, total - window_size + 1)

    page_numbers = list(range(start, end + 1))

    # banderas para primeros/ultimos y puntos suspensivos
    show_first = (1 not in page_numbers)
    show_last = (total not in page_numbers)
    first_page = 1
    last_page = total
    left_has_more = start > 2   # hay hueco entre 1 y start
    right_has_more = end < total - 1

    notificaciones = EventoService.obtener_notificaciones(request.user)

    context = {
        "header_title": "Eventos Publicados",
        "header_paragraph": "Visualiza todos los eventos publicados hasta el momento en SIGEU.",
        "active_page": "eventos-publicados",
        "notificaciones": notificaciones,
        "page_obj": page_obj,
        # datos para paginación
        "page_numbers": page_numbers,
        "show_first": show_first,
        "show_last": show_last,
        "first_page": first_page,
        "last_page": last_page,
        "left_has_more": left_has_more,
        "right_has_more": right_has_more,
    }

    return render(request, "events/eventos_publicados.html", context)

@no_superuser_required
@login_required
@organizador_required
def formulario_edicion(request, pk):
    # Get event by pk
    current_user = request.user
    event = EventoService.obtener_por_id(pk)
    if not event:
        return redirect("not_found")
    elif not EventoService.es_creador(current_user, pk):
        return redirect("forbidden")

    # Only render if it has the status "Borrador" or "Rechazado"
    if event.estado != "Borrador" and event.estado != "Rechazado":
        return redirect("mis_eventos")
    
    # Load initial data for event form
    initial_data = {
        "nombre": event.nombre,
        "tipo": event.tipo,
        "descripcion": event.descripcion,
        "capacidad": event.capacidad,
        "fecha_inicio": event.fecha_inicio.strftime('%Y-%m-%d') if event.fecha_inicio else None,
        "fecha_fin": event.fecha_fin.strftime('%Y-%m-%d') if event.fecha_fin else None,
        "hora_inicio": event.hora_inicio,
        "hora_fin": event.hora_fin,
    }

    mainForm = RegistroEventoForm(initial=initial_data)

    # Search Forms
    modalBuscarInstalacionesForm = ModalBuscarInstalacionForm()
    modalBuscarOrganizadoresForm = ModalBuscarOrganizadorForm()
    modalBuscarOrganizacionesForm = ModalBuscarOrganizacionForm()

    # Assignment forms
    modalAsociarOrganizadorForm = OrganizadorEventoForm()
    modalAsociarOrganizacionForm = OrganizacionInvitadaForm()

    # External organization creation form
    registroOrganizacionForm = RegistroForm()

    notificaciones = EventoService.obtener_notificaciones(request.user)

    return render(request, "events/registro_evento.html", {
        "page__title": "SIGEU | Edición Evento",
        "header_title": "Editar Evento Universitario", 
        "header_paragraph": "Administra las entidades que participan en tus eventos. Organiza y lleva el control de todos tus eventos en un solo lugar",
        "notificaciones": notificaciones,
        "is_editing": True,
        "form": mainForm,
        "modal_buscar_instalaciones_form": modalBuscarInstalacionesForm,
        "modal_buscar_organizadores_form": modalBuscarOrganizadoresForm,
        "modal_buscar_organizaciones_form": modalBuscarOrganizacionesForm,
        "modal_asociar_organizador_form": modalAsociarOrganizadorForm,
        "modal_asociar_organizacion_form": modalAsociarOrganizacionForm,
        "registro_organizacion_form": registroOrganizacionForm,
        "current_user_data": { "id": current_user.id_usuario, "nombreCompleto": f"{current_user.nombres} {current_user.apellidos}", "rol": current_user.rol },
        "active_page": "mis-eventos",
    })