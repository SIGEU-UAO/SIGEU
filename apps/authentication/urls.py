from django.urls import path
from . import views

urlpatterns = [
    # --- FBV ---
    path("registro/", views.formulario_registro, name="registro"),     
    path("inicio-sesion/", views.inicio_sesion, name="inicio_sesion"),    
    path("dashboard/", views.inicio_sesion, name="dashboard"),            

    # --- CBV ---
    path("registro/api/", views.registroAPI.as_view(), name="registro_api"),
    path("inicio-sesion/api/", views.inicio_sesionAPI.as_view(), name="inicio_sesion_api"),
]
