from ...models import Estudiante

class EstudianteService:
    @staticmethod
    def list():
        return Estudiante.objects.all()

    @staticmethod
    def get_by_usuario(usuario_id):
        try:
            return Estudiante.objects.get(usuario_id=usuario_id)
        except Estudiante.DoesNotExist:
            return None

    @staticmethod
    def get_by_codigo(codigo):
        try:
            return Estudiante.objects.get(codigo_estudiante=codigo)
        except Estudiante.DoesNotExist:
            return None

    @staticmethod
    def create(usuario_id, codigo_estudiante, programa_id):
        return Estudiante.objects.create(
            usuario_id=usuario_id,
            codigo_estudiante=codigo_estudiante,
            programa_id=programa_id
        )

    @staticmethod
    def delete_by_usuario(usuario_id):
        return Estudiante.objects.filter(usuario_id=usuario_id).delete()
