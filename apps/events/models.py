from django.db import models
from apps.core.models import InstalacionFisica
from apps.users.models import Usuario
from apps.external_organizations.models import OrganizacionExterna
from .utils import *
from django.core.validators import MinLengthValidator
import datetime

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
    capacidad = models.IntegerField()
    fechaInicio = models.DateField()
    fechaFin = models.DateField(default=datetime.date.today)
    horaInicio = models.TimeField() 
    horaFin = models.TimeField()
    creador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="eventos_creados")
    fecha_ultimo_cambio = models.DateTimeField(auto_now=True)
    fechaEnvio = models.DateTimeField(default=None, null=True, blank=True)
    notificacionEnvioLeida = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre} - {self.tipo} ({ self.estado })"
    
    @property
    def organizadores_ordenados(self):
        organizadores = list(self.organizadores_asignados.all())
        organizadores.sort(key=lambda o: 0 if o.organizador == self.creador else 1)
        return organizadores
    
    class Meta:
        db_table = "eventos"
        verbose_name = "evento"
        verbose_name_plural = "eventos"

class InstalacionAsignada(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name="instalaciones_asignadas")
    instalacion = models.ForeignKey(InstalacionFisica, on_delete=models.CASCADE, related_name="eventos_asignados")
    
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

class OrganizadorEvento(models.Model):
    # Enumerations
    TIPOS = [ 
        ("director_programa", "Director del Programa"),
        ("director_docencia", "Director de Docencia")
    ]
    
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name="organizadores_asignados")
    organizador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="eventos_organizados")
    aval = models.FileField(upload_to=path_coordinador_aval) 
    tipo = models.CharField(max_length=50, choices=TIPOS)
    
    # Simular PK Compuesta
    class Meta:
        db_table = "organizadores_eventos"
        verbose_name = "organizador_evento"
        verbose_name_plural = "organizadores_eventos"
        constraints = [
            models.UniqueConstraint(
                fields=['evento', 'organizador'],
                name='unique_evento_organizador'
            )
        ]

class OrganizacionInvitada(models.Model):    
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name="organizaciones_invitadas")
    organizacion = models.ForeignKey(OrganizacionExterna, on_delete=models.CASCADE, related_name="eventos_invitados")
    representante_asiste = models.BooleanField(default=False, verbose_name="¿Representante legal asiste?")
    representante_alterno = models.CharField(max_length=100, null=True, blank=True)
    certificado_participacion = models.FileField(upload_to=path_organizacion_certificado) 
    
    # Simular PK Compuesta
    class Meta:
        db_table = "organizaciones_invitadas"
        verbose_name = "organizacion_invitada"
        verbose_name_plural = "organizaciones_invitadas"
        constraints = [
            models.UniqueConstraint(
                fields=['evento', 'organizacion'],
                name='unique_evento_organizacion'
            )
        ]

class EvaluacionEvento(models.Model):
    # Enumerations
    TIPOS_EVALUACION = [
        ("aprobacion", "Aprobación"),
        ("rechazo", "Rechazo")
    ]
    
    idEvaluacion = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name="evaluaciones")
    evaluador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="evaluaciones")
    fechaEvaluacion = models.DateTimeField(auto_now_add=True)
    tipoEvaluacion = models.CharField(max_length=10, choices=TIPOS_EVALUACION)
    justificacion = models.TextField(validators=[MinLengthValidator(10)])
    acta = models.FileField(upload_to=path_acta)
    notificacionLeida = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.evento} - {self.tipoEvaluacion}"

    class Meta:
        db_table = "evaluaciones_eventos"
        verbose_name = "evaluacion_evento"
        verbose_name_plural = "evaluaciones_eventos"