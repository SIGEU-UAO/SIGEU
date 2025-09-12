from django.db import transaction
from ..models import Secretaria

class SecretariaService:
    @staticmethod
    def list():
        # une usuario + facultad
        return Secretaria.objects.select_related("usuario", "facultad").all()

    @staticmethod
    def get_by_usuario(usuario_id):
        # usuario_id = PK de Usuario (idUsuario)
        return Secretaria.objects.select_related("usuario", "facultad").filter(usuario_id=usuario_id).first()

    @staticmethod
    @transaction.atomic  # opcional
    def create(usuario_id, facultad_id):
        """
        facultad_id = PK de Facultad (en tu modelo: idUsuario)
        Django lo guarda en la columna 'facultad_id'
        """
        return Secretaria.objects.create(
            usuario_id=usuario_id,
            facultad_id=facultad_id
        )

    @staticmethod
    @transaction.atomic  # opcional
    def delete_by_usuario(usuario_id):
        deleted= Secretaria.objects.filter(usuario_id=usuario_id).delete()
        return deleted
