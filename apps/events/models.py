from django.db import models
from apps.users.models import Usuario

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
    descripcion = models.TextField()
    nombre = models.CharField(max_length=100)
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