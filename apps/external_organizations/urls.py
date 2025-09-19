from django.urls import path
from . import views

urlpatterns = [
    # --- Views ---
    path("orgs/registro/", views.formulario_registro, name="registrar_org"),            

    # --- API ---
    #path("users/api/registro/", UsersAPI.registro, name="registro_api")
]