from ...models import Estudiante

class EstudianteService:
    @staticmethod
    def list():
        # I return the queryset as-is; we can add joins later if we need them.
        return Estudiante.objects.all()

    @staticmethod
    def get_by_usuario(usuario_id):
        # OneToOne with Usuario; .get() is perfect. I return None when missing.
        try:
            return Estudiante.objects.get(usuario_id=usuario_id)
        except Estudiante.DoesNotExist:
            return None

    @staticmethod
    def get_by_codigo(codigo):
        # 'codigo_estudiante' is unique, so .get() is safe here.
        try:
            return Estudiante.objects.get(codigo_estudiante=codigo)
        except Estudiante.DoesNotExist:
            return None

    @staticmethod
    def create(usuario_id, codigo_estudiante, programa_id):
        # I create by passing FK ids directly; Django handles the *_id convention.
        return Estudiante.objects.create(
            usuario_id=usuario_id,
            codigo_estudiante=codigo_estudiante,
            programa_id=programa_id
        )

    @staticmethod
    def delete_by_usuario(usuario_id):
        # Delete by the OneToOne FK; pass through ORM delete result.
        return Estudiante.objects.filter(usuario_id=usuario_id).delete()
