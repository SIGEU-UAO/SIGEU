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
    path("eventos/enviados/", views.eventos_enviados, name="eventos_enviados"),

    # --- API ---
    path("eventos/api/registro/", EventoAPI.registro, name="registro_evento_api"),
    path('eventos/api/listado-eventos/', EventoAPI.mis_eventos, name='mis_eventos_api'),
    path('eventos/api/editar/<int:id>/', EventoAPI.actualizar, name="actualizar_evento_api"),
    path('eventos/api/eliminar/<int:id_evento>/', EventoAPI.eliminar_evento, name='eliminar_evento_api'),

    path("eventos/api/asignar-instalaciones/", InstalacionesAsignadasAPI.asignar_instalaciones_fisicas, name="asignar_instalaciones_api"),
    path("eventos/api/listar-instalaciones/<int:eventoId>/", InstalacionesAsignadasAPI.listar_instalaciones_asignadas, name="listar_instalaciones_api"),
    path("eventos/api/actualizar-instalaciones/<int:eventoId>/", InstalacionesAsignadasAPI.actualizar_instalaciones_fisicas, name="actualizar_instalaciones_api"),

    path("eventos/api/asignar-organizadores/", OrganizadorEventoAPI.asignar_organizadores_evento, name="asignar_organizadores_api"),
    path("eventos/api/listar-organizadores/<int:eventoId>/", OrganizadorEventoAPI.listar_organizadores, name="listar_organizadores_api"),
    path("eventos/api/actualizar-organizadores/<int:eventoId>/", OrganizadorEventoAPI.actualizar_organizadores, name="actualizar_organizadores_api"),

    path("eventos/api/asignar-organizaciones/", OrganizacionInvitadaAPI.asignar_organizaciones_invitadas, name="asignar_organizaciones_api"),
    path("eventos/api/listar-organizaciones/<int:eventoId>/", OrganizacionInvitadaAPI.listar_organizaciones_invitadas, name="listar_organizaciones_invitadas_api"),
    path("eventos/api/actualizar-organizaciones/<int:eventoId>/", OrganizacionInvitadaAPI.actualizar_organizaciones, name="actualizar_organizaciones_api"),

    path("eventos/api/enviar-validacion/<int:id_evento>/",EventoAPI.enviar_evento_validacion,name="enviar_evento_validacion_api"),
    path("eventos/api/listar-enviados/",EventoAPI.listar_eventos_enviados,name="listar_eventos_enviados_api"),
    path("eventos/api/obtener-datos-organizador/<int:id_evento>/<int:id_organizador>/",EventoAPI.obtener_datos_organizador,name="obtener_datos_organizador_api"),
    path("eventos/api/obtener-datos-organizacion-invitada/<int:id_evento>/<int:id_organizacion>/",EventoAPI.obtener_datos_organizacion_invitada,name="obtener_datos_orginvitada_api"),
    
    path("eventos/api/aprobar-evento/<int:id_evento>/",EventoAPI.aprobar_evento,name="aprobar_evento_api"),
    path("eventos/api/rechazar-evento/<int:id_evento>/",EventoAPI.rechazar_evento,name="rechazar_evento_api"),
    path("eventos/api/marcar-notificacion-como-leida/<int:id_registro>/",EventoAPI.marcar_como_leida,name="marcar_notificacion_como_leida_api"),
]