from django.urls import path
from . import views
from .api import AuthAPI

urlpatterns = [
    # --- Views ---
    path("auth/registro/", views.formulario_registro, name="registro"),     
    path("auth/inicio-sesion/", views.inicio_sesion, name="inicio_sesion"),    
    path("dashboard/", views.dashboard, name="dashboard"),            

    # --- API ---
    path("auth/api/registro/", AuthAPI.registro, name="registro_api"),
    path("auth/api/inicio-sesion/", AuthAPI.login, name="inicio_sesion_api"),
]
