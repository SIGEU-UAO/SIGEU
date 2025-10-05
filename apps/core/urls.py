from django.urls import path
from .views import get_csrf_token
from .api import CoreAPI

urlpatterns = [
    # --- CSRFToken ---
    path('get-csrf-token/', get_csrf_token, name='get-csrf-token'),

    # --- API ---
    path("instalaciones/api/", CoreAPI.listar, name="instalaciones_api_list"),
]
