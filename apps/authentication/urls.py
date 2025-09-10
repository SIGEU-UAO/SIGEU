from django.urls import path
from . import views

urlpatterns = [
    path("registro", views.formulario_registro, name="formulario_registro")
]
