from django.urls import path
from . import views
from .api import UsersAPI

urlpatterns = [
    # --- Views ---
    path("users/registro/", views.formulario_registro, name="registro"),     
    path("users/inicio-sesion/", views.inicio_sesion, name="inicio_sesion"),    
    path("dashboard/", views.dashboard, name="dashboard"),            

    # --- API ---
    path("users/api/registro/", UsersAPI.registro, name="registro_api"),
    path("users/api/inicio-sesion/", UsersAPI.login, name="inicio_sesion_api"),
    path("users/api/logout/", UsersAPI.logout, name="logout"),

    # --- API ORGANIZADORES ---
    path("organizadores/api/", UsersAPI.listar_organizadores, name="organizadores_api_list"),
    path("organizadores/api/<int:id>/", UsersAPI.obtener_por_id, name="organizadores_api_obtener_por_id"),
]
