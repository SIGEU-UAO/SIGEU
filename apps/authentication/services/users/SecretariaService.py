from ...models import Secretaria

class SecretariaService:
    @staticmethod
    def list():
        # Straightforward list; no eager joins here to keep it simple.
        return Secretaria.objects.all()

    @staticmethod
    def get_by_usuario(usuario_id):
        # This is a OneToOne with Usuario, so .get() is a good fit.
        # I return None when it's not found so callers can decide what to do.
        try:
            return Secretaria.objects.get(usuario_id=usuario_id)
        except Secretaria.DoesNotExist:
            return None

    @staticmethod
    def create(usuario_id, facultad_id):
        # Note to the team: in our Facultad model, the PK field is named 'idUsuario'
        # (weird name for a faculty PK, but it's our current schema). Django still expects
        # we pass 'facultad_id' with that PK value.
        return Secretaria.objects.create(
            usuario_id=usuario_id,
            facultad_id=facultad_id
        )

    @staticmethod
    def delete_by_usuario(usuario_id):
        # Delete by the OneToOne FK; returns (count, details).
        return Secretaria.objects.filter(usuario_id=usuario_id).delete()
