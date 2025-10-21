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
    path("eventos/editar/<int:pk>/", views.formulario_edicion, name="editar_evento"),

    # --- API ---
    path("eventos/api/registro/", EventoAPI.registro, name="registro_evento_api"),
    path('eventos/api/listado-eventos/', EventoAPI.mis_eventos, name='mis_eventos_api'),
    path('eventos/api/editar/<int:id>/', EventoAPI.actualizar, name="actualizar_evento_api"),

    path("eventos/api/asignar-instalaciones/", InstalacionesAsignadasAPI.asignar_instalaciones_fisicas, name="asignar_instalaciones_api"),
    path("eventos/api/listar-instalaciones/<int:eventoId>/", InstalacionesAsignadasAPI.listar_instalaciones_asignadas, name="listar_instalaciones_api"),
    path("eventos/api/actualizar-instalaciones/<int:eventoId>/", InstalacionesAsignadasAPI.actualizar_instalaciones_fisicas, name="actualizar_instalaciones_api"),

    path("eventos/api/asignar-organizadores/", OrganizadorEventoAPI.asignar_organizadores_evento, name="asignar_organizadores_api"),
    path("eventos/api/listar-organizadores/<int:eventoId>/", OrganizadorEventoAPI.listar_organizadores, name="listar_organizadores_api"),

    path("eventos/api/asignar-organizaciones/", OrganizacionInvitadaAPI.asignar_organizaciones_invitadas, name="asignar_organizaciones_api"),


    path("eventos/api/editar/<int:id>/", EventoAPI.actualizar, name="actualizar_evento_api"),
]