from ..models import UnidadAcademica

class UnidadAcademicaService:
    @staticmethod
    def list():
        # I'm keeping this simple: I return all records without joins,
        # because we don't need eager loading (no select_related) for our current use.
        return UnidadAcademica.objects.all()

    @staticmethod
    def get(unidad_id):
        # I prefer .get() so I don't need .first(); if not found, I return None.
        try:
            return UnidadAcademica.objects.get(idUnidadAcademica=unidad_id)
        except UnidadAcademica.DoesNotExist:
            return None

    @staticmethod
    def create(nombre, facultad_id):
        # I create the record by passing the FK as *_id; Django maps it correctly.
        return UnidadAcademica.objects.create(nombre=nombre, facultad_id=facultad_id)

    @staticmethod
    def update(unidad_id, nombre=None, facultad_id=None):
        # I reuse get(); if it doesn't exist, I return None so the view can 404/400.
        unidad_academica = UnidadAcademicaService.get(unidad_id)
        if not unidad_academica:
            return None
        # Only update the fields that were provided.
        if nombre is not None:
            unidad_academica.nombre = nombre
        if facultad_id is not None:
            unidad_academica.facultad_id = facultad_id
        unidad_academica.save()
        return unidad_academica

    @staticmethod
    def delete(unidad_id):
        # I delete by PK; delete() returns (count, details) – we just pass it through.
        return UnidadAcademica.objects.filter(idUnidadAcademica=unidad_id).delete()
