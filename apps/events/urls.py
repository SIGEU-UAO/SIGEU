from django.urls import path
from . import views
from .api.event import EventoAPI
from .api.associations.instalacion_fisica import InstalacionesAsignadasAPI
from .api.associations.organizador_evento import OrganizadorEventoAPI
from .api.associations.organizaciones_invitadas import OrganizacionInvitadaAPI

urlpatterns = [
    # --- Views ---
    path("eventos/registro/", views.formulario_registro, name="registrar_evento"),  
    path("eventos/mis-eventos/", views.mis_eventos, name="mis_eventos"),     

    # --- API ---
    path("eventos/api/registro/", EventoAPI.registro, name="registro_evento_api"),
    path('eventos/api/listado-eventos/', EventoAPI.mis_eventos, name='mis_eventos_api'),
    path("eventos/api/asignar-instalaciones/", InstalacionesAsignadasAPI.asignar_instalaciones_fisicas, name="asignar_instalaciones_api"),
    path("eventos/api/asignar-organizadores/", OrganizadorEventoAPI.asignar_coordinadores_evento, name="asignar_coordinadores_api"),
    path("eventos/api/asignar-organizaciones/", OrganizacionInvitadaAPI.asignar_organizaciones_invitadas, name="asignar_organizaciones_api"),
    path("eventos/api/enviar-validacion/<int:id_evento>/",EventoAPI.enviar_evento_validacion,name="enviar_evento_validacion_api"),
    path('eventos/api/eliminar/<int:id_evento>/', EventoAPI.eliminar_evento, name='eliminar_evento_api')
]