from django.urls import path
from . import views
from .api import registro, login

urlpatterns = [
    # --- FBV ---
    path("registro/", views.formulario_registro, name="registro"),     
    path("inicio-sesion/", views.inicio_sesion, name="inicio_sesion"),    
    path("dashboard/", views.dashboard, name="dashboard"),            

    # --- CBV ---
    path("registro/api/", registro.registroAPI.as_view(), name="registro_api"),
    path("inicio-sesion/api/", login.inicio_sesionAPI.as_view(), name="inicio_sesion_api"),
]
