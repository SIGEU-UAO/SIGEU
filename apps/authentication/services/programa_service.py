from ..models import Programa

class ProgramaService:
    @staticmethod
    def list():
        # select_related("facultad") hace JOIN para traer la Facultad en la misma query
        return Programa.objects.select_related("facultad").all()

    @staticmethod
    def get(programa_id):
        # idPrograma es el PK de Programa (según tu modelo)
        return Programa.objects.select_related("facultad").filter(idPrograma=programa_id).first()

    @staticmethod
    def create(nombre, facultad_id):
        """
        facultad_id = valor del PK de Facultad
        IMPORTANTE: Django crea automáticamente el campo FK como 'facultad_id'
        que debe apuntar al PK real de Facultad (en tu modelo es idUsuario)
        """
        return Programa.objects.create(nombre=nombre, facultad_id=facultad_id)

    @staticmethod
    def update(programa_id, nombre=None, facultad_id=None):
        prog = ProgramaService.get(programa_id)
        if not prog:
            return None
        # cambios opcionales
        if nombre is not None:
            prog.nombre = nombre
        if facultad_id is not None:
            # reasigna la FK. Django entiende que esto va a la columna 'facultad_id'
            prog.facultad_id = facultad_id
        prog.save()
        return prog

    @staticmethod
    def delete(programa_id):
        deleted = Programa.objects.filter(idPrograma=programa_id).delete()
        return deleted
