from django.urls import path
from . import views
from .api import UsersAPI

urlpatterns = [
    # --- Views ---
    path("users/registro/", views.formulario_registro, name="registro"),     
    path("users/inicio-sesion/", views.inicio_sesion, name="inicio_sesion"),    
    path("dashboard/", views.dashboard, name="dashboard"),       
    path("perfil/", views.editar_perfil, name="perfil"),

    # --- API ---
    path("users/api/registro/", UsersAPI.registro, name="registro_api"),
    path("users/api/inicio-sesion/", UsersAPI.login, name="inicio_sesion_api"),
    path("users/api/logout/", UsersAPI.logout, name="logout"),
    path("users/api/editar-perfil/", UsersAPI.editar_perfil, name="perfil"),
]
