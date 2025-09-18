from ..models import UnidadAcademica

class UnidadAcademicaService:
    @staticmethod
    def list():
        return UnidadAcademica.objects.all()

    @staticmethod
    def get(unidad_id):
        try:
            return UnidadAcademica.objects.get(idUnidadAcademica=unidad_id)
        except UnidadAcademica.DoesNotExist:
            return None