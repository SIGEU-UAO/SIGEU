from django.urls import path
from . import views
from .api import OrganizacionesExternasAPI

urlpatterns = [
    # --- Views ---
    path("orgs/listado/", views.listado, name="listado_orgs"),
    path("orgs/listado/orgs/editar/<int:pk>/", views.editar, name="editar_org"),
    path("orgs/listado/error/no-encontrada/", views.org_no_encontrada, name="org_no_encontrada"),

    # --- API ---
    path("orgs/api/", OrganizacionesExternasAPI.listar, name="orgs_api_list"),
    path("orgs/api/<int:id>/", OrganizacionesExternasAPI.obtener_por_id, name="orgs_api_obtener_por_id"),
    path("orgs/api/datatables/", OrganizacionesExternasAPI.datatables_rendering, name="orgs_api_datatables"),
    path("orgs/api/registro/", OrganizacionesExternasAPI.registro, name="orgs_registro_api"),
    path("orgs/api/<int:id>/update/", OrganizacionesExternasAPI.actualizar, name="orgs_api_update"),
]
