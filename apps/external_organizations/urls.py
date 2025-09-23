from django.urls import path
from . import views
from .api import OrganizacionesExternasAPI

urlpatterns = [
    # --- Views ---
    path("orgs/registro/", views.formulario_registro, name="registrar_org"),            

    # --- API ---
    path("orgs/api/", OrganizacionesExternasAPI.listar, name="orgs_api_list"),
    path("orgs/api/registro/", OrganizacionesExternasAPI.registro, name="orgs_registro_api"),
]