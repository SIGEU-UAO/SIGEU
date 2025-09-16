from ...models import Secretaria

class SecretariaService:
    @staticmethod
    def list():
        return Secretaria.objects.all()

    @staticmethod
    def get_by_usuario(usuario_id):
        try:
            return Secretaria.objects.get(usuario_id=usuario_id)
        except Secretaria.DoesNotExist:
            return None

    @staticmethod
    def create(usuario_id, facultad_id):
        return Secretaria.objects.create(
            usuario_id=usuario_id,
            facultad_id=facultad_id
        )

    @staticmethod
    def delete_by_usuario(usuario_id):
        return Secretaria.objects.filter(usuario_id=usuario_id).delete()
