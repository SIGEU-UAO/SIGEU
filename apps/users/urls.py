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
    path("users/api/editar-perfil/", UsersAPI.editar_perfil, name="perfil   _api"),

    # --- API ORGANIZADORES ---
    path("organizadores/api/", UsersAPI.listar_organizadores, name="organizadores_api_list"),
    path("organizadores/api/<int:id>/", UsersAPI.obtener_organizador_por_id, name="organizadores_api_obtener_por_id"),

    # Password Reset URLs
    path('reset/password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('reset/password_reset_done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
