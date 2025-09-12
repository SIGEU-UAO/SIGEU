from django.db import transaction
from ..models import Estudiante

class EstudianteService:
    @staticmethod
    def list():
        # select_related para traer usuario y programa en la misma consulta
        return Estudiante.objects.select_related("usuario", "programa").all()

    @staticmethod
    def get_by_usuario(usuario_id):
        # usuario_id = PK del Usuario (idUsuario) al que está ligado vía OneToOne
        return Estudiante.objects.select_related("usuario", "programa").filter(usuario_id=usuario_id).first()

    @staticmethod
    def get_by_codigo(codigo):
        # busca por el código único del estudiante
        return Estudiante.objects.select_related("usuario", "programa").filter(codigo_estudiante=codigo).first()

    @staticmethod
    @transaction.atomic  # opcional (un solo insert); lo dejamos por simetría
    def create(usuario_id, codigo_estudiante, programa_id):
        """
        usuario_id = PK de Usuario (idUsuario) para el OneToOne
        programa_id = PK de Programa (idPrograma). Django lo mapea a 'programa_id' en BD
        """
        return Estudiante.objects.create(
            usuario_id=usuario_id,
            codigo_estudiante=codigo_estudiante,
            programa_id=programa_id
        )

    @staticmethod
    @transaction.atomic  # opcional; mantiene consistencia si hay lógica adicional futura
    def delete_by_usuario(usuario_id):
        deleted = Estudiante.objects.filter(usuario_id=usuario_id).delete()
        return deleted
