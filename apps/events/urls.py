from django.urls import path
from . import views
from .api.organizadorAPI import OrganizadorAPI

urlpatterns = [
    # --- Views ---
    path("eventos/registro/", views.formulario_registro, name="registrar_evento"),           

    # --- API ---
    path("eventos/api/registro/", OrganizadorAPI.registro, name="registro_evento_api"),
]