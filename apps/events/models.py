from django.db import models
from apps.users.models import Usuario
from apps.core.models import InstalacionFisica

class Evento(models.Model):
    # Enumerations
    ESTADOS = [ 
        ("Borrador", "Borrador"),
        ("Enviado", "Enviado"),
        ("Aprobado", "Aprobado"),
        ("Rechazado", "Rechazado"),
    ]

    TIPOS = [
        ("Ludico", "Lúdico"),
        ("Academico", "Académico")
    ]

    # Fields
    idEvento = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    estado = models.CharField(max_length=10, choices=ESTADOS, default="Borrador")
    tipo = models.CharField(max_length=100, choices=TIPOS)
    fecha = models.DateField()
    horaInicio = models.TimeField()
    horaFin = models.TimeField()
    creador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="eventos_creados")

    def __str__(self):
        return f"{self.nombre} - {self.tipo} ({ self.estado })"
    
    class Meta:
        db_table = "eventos"
        verbose_name = "evento"
        verbose_name_plural = "eventos"

class InstalacionesAsignadas(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    instalacion = models.ForeignKey(InstalacionFisica, on_delete=models.CASCADE)
    
    # Simular PK Compuesta
    class Meta:
        db_table = "instalaciones_asignadas"
        verbose_name = "instalacion_asignada"
        verbose_name_plural = "instalaciones_asignadas"
        constraints = [
            models.UniqueConstraint(
                fields=['evento', 'instalacion'],
                name='unique_evento_instalacion'
            )
        ]