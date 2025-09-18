from django.urls import path
from . import views
from .api import registro, login

urlpatterns = [
    # --- FBV ---
    path("auth/registro/", views.formulario_registro, name="registro"),     
    path("auth/inicio-sesion/", views.inicio_sesion, name="inicio_sesion"),    
    path("dashboard/", views.dashboard, name="dashboard"),            

    # --- CBV ---
    path("auth/registro/api/", registro.registroAPI.as_view(), name="registro_api"),
    path("auth/inicio-sesion/api/", login.inicio_sesionAPI.as_view(), name="inicio_sesion_api"),
]
