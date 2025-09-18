from ...models import Docente

class DocenteService:
    @staticmethod
    def list():
        return Docente.objects.all()

    @staticmethod
    def get_by_usuario(usuario_id):
        try:
            return Docente.objects.get(usuario_id=usuario_id)
        except Docente.DoesNotExist:
            return None

    @staticmethod
    def create(usuario_id, unidad_academica_id):
        return Docente.objects.create(
            usuario_id=usuario_id,
            unidadAcademica_id=unidad_academica_id
        )

    @staticmethod
    def delete_by_usuario(usuario_id):
        return Docente.objects.filter(usuario_id=usuario_id).delete()
