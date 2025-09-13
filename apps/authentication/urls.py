from django.urls import path
from . import views

urlpatterns = [
    path("registro/", views.formulario_registro, name="registro"),
    path("inicio-sesion/", views.inicio_sesion, name="inicio_sesion"),
]
