from django.urls import path
from .views import *
from .api import CoreAPI

urlpatterns = [
    # --- CSRFToken ---
    path('get-csrf-token/', get_csrf_token, name='get-csrf-token'),

    # --- Home Page ---
    path('', index, name='index'),

    # --- Error Pages ---
    path('errors/not-found/', not_found, name='not_found'),
    path('errors/forbidden/', forbidden, name='forbidden'),

    # --- API ---
    path("instalaciones/api/", CoreAPI.listar, name="instalaciones_api_list"),
]