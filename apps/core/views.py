from django.shortcuts import render
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.contrib.auth.decorators import login_required
from apps.events.services.event import EventoService
from sigeu.decorators import no_superuser_required
from datetime import datetime

def get_csrf_token(request):
    response = JsonResponse({'csrfToken': get_token(request)})
    response.set_cookie('csrftoken', get_token(request))
    return response

def index(request):
    current_year = datetime.now().year
    return render(request, "core/index.html", {
        "current_year": current_year,
    })

@no_superuser_required
@login_required
def not_found(request):
    notificaciones = EventoService.obtener_notificaciones(request.user)

    return render(request, "errors/error.html", {
        "page__title": "SIGEU | Recurso no encontrado",
        "header_title": "Recurso no encontrado",
        "header_paragraph": "El recurso que buscas no existe o no está disponible.",
        "error_illustration": "assets/img/404.webp",
        "active_page": "dashboard",
        "notificaciones": notificaciones,
    })

@no_superuser_required
@login_required
def forbidden(request):
    notificaciones = EventoService.obtener_notificaciones(request.user)
    
    return render(request, "errors/error.html", {
        "page__title": "SIGEU | Acceso restringido",
        "header_title": "Acceso restringido",
        "header_paragraph": "El recurso que buscas requiere permisos especiales.",
        "error_illustration": "assets/img/403.webp",
        "active_page": "dashboard",
        "notificaciones": notificaciones,
    })