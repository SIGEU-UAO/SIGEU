from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from .models import Contrasenia

class PasswordHistoryValidator:
    """
    Validador que verifica que la nueva contraseña no haya sido utilizada anteriormente.
    Este validador revisa TODAS las contraseñas del historial, no solo las últimas 5.
    """
    
    def __init__(self, user=None):
        self.user = user
    
    def __call__(self, password):
        if not self.user:
            return  # Si no hay usuario, no podemos validar el historial
            
        # Obtener TODAS las contraseñas anteriores del usuario
        contrasenias_anteriores = Contrasenia.objects.filter(
            idUsuario=self.user
        ).order_by('-fechaCambio')  # Ordenar por más reciente primero
        
        # Verificar contra todas las contraseñas del historial
        for contrasenia in contrasenias_anteriores:
            if check_password(password, contrasenia.clave):
                raise ValidationError(
                    "No puedes reutilizar una contraseña que ya has usado anteriormente. "
                    "Por favor, elige una contraseña diferente.",
                    code='password_reused'
                )
    
    def get_help_text(self):
        return "Tu nueva contraseña no puede ser igual a ninguna de las contraseñas que has usado anteriormente."


def validate_password_history(password, user=None):
    """
    Función helper para validar el historial de contraseñas.
    Esta función verifica contra TODAS las contraseñas anteriores.
    """
    if not user:
        return
        
    validator = PasswordHistoryValidator(user=user)
    validator(password)