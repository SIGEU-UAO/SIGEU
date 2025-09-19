from django.db import models

class OrganizacionExterna(models.Model):
    idOrganizacion = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    nombre = models.CharField(max_length=100)
    representanteLegal = models.CharField(max_length=100)
    telefono = models.CharField(max_length=10)
    ubicacion = models.CharField(max_length=100)
    sectorEconomico = models.CharField(max_length=100)
    actividadPrincipal = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} - Representante: {self.representanteLegal}"
    
    class Meta:
        db_table = "organizaciones_externas"
        verbose_name = "organizacion_externa"
        verbose_name_plural = "organizaciones_externas"