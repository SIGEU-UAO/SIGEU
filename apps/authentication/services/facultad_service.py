from ..models import Facultad

class FacultadService:
    @staticmethod
    def list():
        # todas las facultades
        return Facultad.objects.all()

    @staticmethod
    def get(facultad_id):
        # OJO: en tu modelo Facultad el PK se llama idUsuario (lo respetamos)
        return Facultad.objects.filter(idUsuario=facultad_id).first()

    @staticmethod
    def create(nombre):
        # crea una Facultad con nombre
        return Facultad.objects.create(nombre=nombre)

    @staticmethod
    def update(facultad_id, nombre):
        fac = FacultadService.get(facultad_id)
        if not fac:
            return None
        fac.nombre = nombre
        # update_fields guarda solo ese campo
        fac.save(update_fields=["nombre"])
        return fac

    @staticmethod
    def delete(facultad_id):
        # borra por el PK real de tu modelo (idUsuario)
        deleted = Facultad.objects.filter(idUsuario=facultad_id).delete()
        return deleted
