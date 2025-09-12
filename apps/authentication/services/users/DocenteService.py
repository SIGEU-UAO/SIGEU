from ...models import Docente

class DocenteService:
    @staticmethod
    def list():
        # Keep it simple: no eager joins; just return the queryset.
        return Docente.objects.all()

    @staticmethod
    def get_by_usuario(usuario_id):
        # OneToOne with Usuario; using .get() and returning None when it's missing.
        try:
            return Docente.objects.get(usuario_id=usuario_id)
        except Docente.DoesNotExist:
            return None

    @staticmethod
    def create(usuario_id, unidad_academica_id):
        # FK column is 'unidadAcademica_id'; passing the id value is enough.
        return Docente.objects.create(
            usuario_id=usuario_id,
            unidadAcademica_id=unidad_academica_id
        )

    @staticmethod
    def delete_by_usuario(usuario_id):
        # Standard delete by FK; returns (count, details).
        return Docente.objects.filter(usuario_id=usuario_id).delete()
