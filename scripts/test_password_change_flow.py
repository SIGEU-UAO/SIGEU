# -*- coding: utf-8 -*-
"""
Prueba no interactiva del flujo de cambio de contraseña en /perfil/
- Crea un usuario de prueba (si no existe)
- Realiza POSTs simulando AJAX al endpoint /perfil/
- Verifica validación de historial y éxito en cambios válidos
"""
import os
import sys
import json
import pathlib
import django

# Asegurar que el proyecto esté en sys.path
BASE_DIR = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sigeu.settings")
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from apps.users.models import Contrasenia

User = get_user_model()

EMAIL = "pruebas.perfil@uao.edu.co"
PASS_INICIAL = "Inicial123"
PASS_NUEVA = "NuevaPass123"
PASS_OTRA = "OtraPass123"

client = Client()

# 1) Crear usuario de prueba si no existe
user, created = User.objects.get_or_create(
    email=EMAIL,
    defaults=dict(
        numeroIdentificacion="12345678",
        nombres="Usuario",
        apellidos="Pruebas",
        telefono="3001234567",
    ),
)
if created:
    user.set_password(PASS_INICIAL)
    user.save()
    # Guardar contraseña inicial en historial
    Contrasenia.objects.create(idUsuario=user, clave=user.password, es_activa=True)
else:
    # Asegurar que tiene una contraseña conocida y un historial consistente
    user.set_password(PASS_INICIAL)
    user.save()
    Contrasenia.objects.filter(idUsuario=user).delete()
    Contrasenia.objects.create(idUsuario=user, clave=user.password, es_activa=True)

# 2) Login
logged = client.login(username=EMAIL, password=PASS_INICIAL)
print("login:", logged)

headers = {"HTTP_X_REQUESTED_WITH": "XMLHttpRequest", "HTTP_HOST": "localhost"}

# Helper para POST a /perfil/
def post_perfil(password_val):
    data = {
        # sólo enviamos la contraseña; el backend rellena los demás campos
        "contraseña": password_val,
    }
    resp = client.post("/perfil/", data, **headers)
    try:
        payload = json.loads(resp.content.decode("utf-8"))
    except Exception:
        payload = {"raw": resp.content.decode("utf-8", errors="ignore")}
    return resp.status_code, payload

# 3) Cambiar a PASS_NUEVA (debe ser éxito)
status1, payload1 = post_perfil(PASS_NUEVA)
print("cambio_1_status:", status1)
print("cambio_1_payload:", payload1)

# Reautenticar con la contraseña nueva (tras cambiar password, la sesión previa se invalida)
client.logout()
logged2 = client.login(username=EMAIL, password=PASS_NUEVA)
print("login_con_nueva:", logged2)

# 4) Reintentar PASS_NUEVA (debe ser rechazado por ser igual a la actual)
status2, payload2 = post_perfil(PASS_NUEVA)
print("reutilizacion_status:", status2)
print("reutilizacion_payload:", payload2)

# 5) Intentar PASS_INICIAL (debe ser rechazado por historial)
status3, payload3 = post_perfil(PASS_INICIAL)
print("reutilizacion_inicial_status:", status3)
print("reutilizacion_inicial_payload:", payload3)

# 6) Intentar PASS_OTRA (debe ser éxito)
status4, payload4 = post_perfil(PASS_OTRA)
print("cambio_2_status:", status4)
print("cambio_2_payload:", payload4)
