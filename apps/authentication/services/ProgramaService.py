from ..models import Programa

class ProgramaService:
    @staticmethod
    def list():
        # Simple list with no select_related; we don't need the join for now.
        return Programa.objects.all()

    @staticmethod
    def get(programa_id):
        # Using .get() so I don't need .first(); I return None if it's not found.
        try:
            return Programa.objects.get(idPrograma=programa_id)
        except Programa.DoesNotExist:
            return None

    @staticmethod
    def create(nombre, facultad_id):
        # Reminder: Django maps FK field to 'facultad_id' in the DB; we pass the PK value here.
        return Programa.objects.create(nombre=nombre, facultad_id=facultad_id)

    @staticmethod
    def update(programa_id, nombre=None, facultad_id=None):
        # I fetch once; if it doesn't exist, I return None and let the view handle it.
        programa = ProgramaService.get(programa_id)
        if not programa:
            return None
        if nombre is not None:
            programa.nombre = nombre
        if facultad_id is not None:
            programa.facultad_id = facultad_id
        programa.save()
        return programa

    @staticmethod
    def delete(programa_id):
        # Delete by real PK (idPrograma); return the ORM's delete tuple.
        return Programa.objects.filter(idPrograma=programa_id).delete()
