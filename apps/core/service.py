from .models import InstalacionFisica

class InstalacionesFisicasService:
    @staticmethod
    def listar():
        return InstalacionFisica.objects.values("ubicacion", "tipo", "capacidad")

    @staticmethod
    def filtrar_por_ubicacion(ubicacion):
        if not ubicacion:
         return []
        return list(
            InstalacionFisica.objects
            .filter(ubicacion__icontains=ubicacion)  
            .values(
                "id_instalacion",   
                "ubicacion",
                "tipo",
                "capacidad"
            )
        )
    
    @staticmethod
    def obtener_por_id(id_instalacion):
        try:
            return InstalacionFisica.objects.get(id_instalacion=id_instalacion)
        except InstalacionFisica.DoesNotExist:
            return False