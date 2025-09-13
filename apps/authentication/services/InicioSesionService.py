from django.contrib.auth import authenticate, login

class InicioSesionService:
    @staticmethod
    def iniciar(request, email, password):
        if not email or not password:
            return {"ok": False, "error": "missing_fields"}
        usuario = authenticate(request, username=email, password=password)
        if usuario is None:
            return {"ok": False, "error": "invalid_credentials"}
        if not usuario.is_active:
            return {"ok": False, "error": "inactive_account"}
        login(request, usuario)

        return {"ok": True, "user_id": getattr(usuario, "idUsuario", usuario.pk)}
