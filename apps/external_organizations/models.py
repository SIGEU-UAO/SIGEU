from django.db import models
from apps.users.models import Usuario

class OrganizacionExterna(models.Model):
    SECTORES_ECONOMICOS_CHOICES = [
        ('Educacion y Ciencia', 'Educación y Ciencia'),
        ('Tecnologia y Comunicaciones', 'Tecnología y Comunicaciones'),
        ('Salud y Bienestar', 'Salud y Bienestar'),
        ('Empresarial e Industrial', 'Empresarial e Industrial'),
        ('Finanzas y Servicios profesionales', 'Finanzas y Servicios Profesionales'),
        ('Cultura y Medios', 'Cultura y Medios'),
        ('Medio Ambiente y Sostenibilidad', 'Medio Ambiente y Sostenibilidad'),
        ('Gobierno y Organismos publicos', 'Gobierno y Organismos Públicos'),
        ('Organizaciones sociales y ONGs', 'Organizaciones Sociales y ONGs'),
        ('Turismo, Hoteleria y Gastronomia', 'Turismo, Hotelería y Gastronomía'),
        ('Comercio y Consumo', 'Comercio y Consumo'),
        ('Otro', 'Otro'),
    ]

    id_organizacion = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    nit = models.CharField(max_length=12, unique=True) 
    nombre = models.CharField(max_length=100)
    representante_legal = models.CharField(max_length=100)
    telefono = models.CharField(max_length=10, unique=True)
    ubicacion = models.CharField(max_length=100)
    sector_economico = models.CharField(max_length=100, choices=SECTORES_ECONOMICOS_CHOICES)
    actividad_principal = models.CharField(max_length=200)
    creador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="organizaciones_creadas")

    def __str__(self):
        return f"{self.nombre} - Representante: {self.representante_legal}"
    
    class Meta:
        db_table = "organizaciones_externas"
        verbose_name = "organizacion_externa"
        verbose_name_plural = "organizaciones_externas"