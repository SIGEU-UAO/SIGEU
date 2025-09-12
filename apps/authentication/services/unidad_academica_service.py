from ..models import UnidadAcademica

class UnidadAcademicaService:
    @staticmethod
    def list():
        # trae unidades + su facultad en un JOIN para evitar N+1
        return UnidadAcademica.objects.select_related("facultad").all()

    @staticmethod
    def get(unidad_id):
        # idUnidadAcademica es el PK de esta tabla en tu modelo
        return UnidadAcademica.objects.select_related("facultad").filter(idUnidadAcademica=unidad_id).first()

    @staticmethod
    def create(nombre, facultad_id):
        """
        facultad_id = PK real de Facultad (en tu modelo: idUsuario)
        al asignarlo a 'facultad_id', Django resuelve la FK correctamente
        """
        return UnidadAcademica.objects.create(nombre=nombre, facultad_id=facultad_id)

    @staticmethod
    def update(unidad_id, nombre=None, facultad_id=None):
        ua = UnidadAcademicaService.get(unidad_id)
        if not ua:
            return None
        if nombre is not None:
            ua.nombre = nombre
        if facultad_id is not None:
            ua.facultad_id = facultad_id
        ua.save()
        return ua

    @staticmethod
    def delete(unidad_id):
        deleted = UnidadAcademica.objects.filter(idUnidadAcademica=unidad_id).delete()
        return deleted
