from django.db import transaction
from ..models import Usuario

class UsuarioService:
    @staticmethod
    def list():
        # devuelve un QuerySet con todos los usuarios (no evalúa hasta iterar)
        return Usuario.objects.all()

    @staticmethod
    def get_by_id(user_id):
        # user_id = valor del PK en tu modelo Usuario (campo: idUsuario)
        # .first() regresa la instancia o None si no existe
        return Usuario.objects.filter(idUsuario=user_id).first()

    @staticmethod
    def get_by_email(email):
        # busca por email único según tu modelo
        return Usuario.objects.filter(email=email).first()

    @staticmethod
    def exists_by_identificacion(numero):
        # True si ya hay un usuario con ese numeroIdentificacion
        return Usuario.objects.filter(numeroIdentificacion=numero).exists()

    @staticmethod
    @transaction.atomic  # opcional en este caso (operación de un solo modelo)
    def create(data):
        """
        data: dict con claves esperadas del modelo Usuario
          - email (USERNAME_FIELD)
          - password (se encripta con el manager)
          - nombres, apellidos, telefono, numeroIdentificacion
        usa Usuario.objects.create_user(...) de tu UsuarioManager
        """
        email = data.get("email")
        password = data.get("password")
        # aquí el manager ya hace set_password (hash seguro)
        usuario = Usuario.objects.create_user(
            email=email,
            password=password,
            nombres=data.get("nombres"),
            apellidos=data.get("apellidos"),
            telefono=data.get("telefono"),
            numeroIdentificacion=data.get("numeroIdentificacion"),
        )
        return usuario

    @staticmethod
    @transaction.atomic  # opcional; útil si en el futuro hay triggers/acciones encadenadas
    def delete(user_id):
        # elimina por PK (idUsuario). deleted es el número de filas borradas
        deleted = Usuario.objects.filter(idUsuario=user_id).delete()
        return deleted
