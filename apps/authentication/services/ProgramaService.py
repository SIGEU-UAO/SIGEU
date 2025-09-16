from ..models import Programa

class ProgramaService:
    def list():
        return Programa.objects.all()


    def get(programa_id):
        try:
            return Programa.objects.get(idPrograma=programa_id)
        except Programa.DoesNotExist:
            return None

   
    

   
   