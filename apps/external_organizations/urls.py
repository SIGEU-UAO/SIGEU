from django.urls import path
from . import views
from .api import OrganizacionesExternasAPI

urlpatterns = [
    # --- Views ---
    path("orgs/registro/", views.formulario_registro, name="registrar_org"),
    path("orgs/listado/", views.listado, name="listado_orgs"),

    # --- API ---
    path("orgs/api/", OrganizacionesExternasAPI.listar, name="orgs_api_list"),
    path("orgs/api/<int:id>/", OrganizacionesExternasAPI.obtener_por_id, name="orgs_api_obtener_por_id"),
    path("orgs/api/datatables/", OrganizacionesExternasAPI.datatables_rendering, name="orgs_api_datatables"),
    path("orgs/api/registro/", OrganizacionesExternasAPI.registro, name="orgs_registro_api"),
]
