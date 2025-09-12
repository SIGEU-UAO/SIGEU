from django.db import transaction
from ..models import Docente

class DocenteService:
    @staticmethod
    def list():
        # une usuario + unidadAcademica para evitar N+1
        return Docente.objects.select_related("usuario", "unidadAcademica").all()

    @staticmethod
    def get_by_usuario(usuario_id):
        # usuario_id = PK de Usuario (idUsuario)
        return Docente.objects.select_related("usuario", "unidadAcademica").filter(usuario_id=usuario_id).first()

    @staticmethod
    @transaction.atomic  # opcional
    def create(usuario_id, unidad_academica_id):
        """
        unidad_academica_id = PK de UnidadAcademica (idUnidadAcademica)
        Django lo guarda en la columna 'unidadAcademica_id'
        """
        return Docente.objects.create(
            usuario_id=usuario_id,
            unidadAcademica_id=unidad_academica_id
        )

    @staticmethod
    @transaction.atomic  # opcional
    def delete_by_usuario(usuario_id):
        deleted = Docente.objects.filter(usuario_id=usuario_id).delete()
        return deleted
