from django.urls import path
from . import views
from .api.event import EventoAPI
from .api.associations.instalacion_fisica import InstalacionesAsignadasAPI
from .api.associations.organizador_evento import OrganizadorEventoAPI

urlpatterns = [
    # --- Views ---
    path("eventos/registro/", views.formulario_registro, name="registrar_evento"),           

    # --- API ---
    path("eventos/api/registro/", EventoAPI.registro, name="registro_evento_api"),
    path("eventos/api/asignar-instalaciones/", InstalacionesAsignadasAPI.asignar_instalaciones_fisicas, name="asignar_instalaciones_api"),
    path("eventos/api/asignar-organizadores/", OrganizadorEventoAPI.asignar_coordinadores_evento, name="asignar_coordinadores_api")
]