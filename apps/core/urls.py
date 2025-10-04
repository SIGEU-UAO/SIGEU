from django.urls import path
from .api import CoreAPI

urlpatterns = [
    # --- API ---
    path("instalaciones/api/", CoreAPI.listar, name="instalaciones_api_list"),
]
