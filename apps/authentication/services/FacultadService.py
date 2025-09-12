from ..models import Facultad

class FacultadService:
    @staticmethod
    def list():
        # All faculties; nothing fancy here.
        return Facultad.objects.all()

    @staticmethod
    def get(facultad_id):
        # Heads-up: in our model the PK is named 'idUsuario'.
        # I use .get() and return None if it doesn't exist.
        try:
            return Facultad.objects.get(idUsuario=facultad_id)
        except Facultad.DoesNotExist:
            return None

    @staticmethod
    def create(nombre):
        # Minimal create with the 'nombre' field only.
        return Facultad.objects.create(nombre=nombre)

    @staticmethod
    def update(facultad_id, nombre):
        # I look it up once; if it's not there, I return None.
        facultad = FacultadService.get(facultad_id)
        if not facultad:
            return None
        facultad.nombre = nombre
        # I could use update_fields for efficiency, but save() is fine and clear.
        facultad.save(update_fields=["nombre"])
        return facultad

    @staticmethod
    def delete(facultad_id):
        # Delete by the actual PK field in our model ('idUsuario').
        return Facultad.objects.filter(idUsuario=facultad_id).delete()
