from django.db import IntegrityError
from .models import InstalacionFisica

class InstalacionesFisicasService:
    @staticmethod
    def listar():
        return InstalacionFisica.objects.values()

    @staticmethod
    def filtrar_por_ubicacion(ubicacion):
        if not ubicacion:
         return []
        return list(
            InstalacionFisica.objects
            .filter(ubicacion__icontains=ubicacion)  
            .values(
                "idInstalacion",   
                "ubicacion",
                "tipo",
                "capacidad"
            )
        )
    
    @staticmethod
    def obtener_por_id(id_instalacion):
        return InstalacionFisica.objects.get(idInstalacion=id_instalacion)