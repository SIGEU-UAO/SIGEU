from ..models import Facultad

class FacultadService:
    @staticmethod
    def list():
        return Facultad.objects.all()

    @staticmethod
    def get(facultad_id):
        try:
            return Facultad.objects.get(idUsuario=facultad_id)
        except Facultad.DoesNotExist:
            return None