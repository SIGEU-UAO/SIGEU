from django.core.validators import MinValueValidator
from django.db import models

class Facultad(models.Model):
    id_facultad = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = "facultades"
        verbose_name = "facultad"
        verbose_name_plural = "facultades"

class Programa(models.Model):
    id_programa = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    facultad = models.ForeignKey(Facultad, on_delete=models.CASCADE, related_name="programas")
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} (Facultad: {self.facultad.nombre})"
    
    class Meta:
        db_table = "programas"

class UnidadAcademica(models.Model):
    id_unidad_academica = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    facultad = models.ForeignKey(Facultad, on_delete=models.CASCADE, related_name="unidades_academicas")
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} (Facultad: {self.facultad.nombre})"

    class Meta:
        db_table = "unidades_academicas"
        verbose_name = "unidad_academica"
        verbose_name_plural = "unidades_academicas"

class InstalacionFisica(models.Model):
    # Enumerations
    TIPOS = [ 
        ("Salon", "Salón"),
        ("Auditorio", "Auditorio"),
        ("Laboratorio", "Laboratorio"),
        ("Cancha", "Cancha"),
    ]
    
    #Fields
    id_instalacion = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    ubicacion = models.CharField(max_length=100)
    capacidad = models.IntegerField(validators=[MinValueValidator(0)])
    tipo = models.CharField(max_length=11, choices=TIPOS)

    def __str__(self):
        return f"{self.ubicacion} ({self.tipo}) - {self.capacidad} personas"

    class Meta:
        db_table = "instalaciones_fisicas"
        verbose_name = "instalacion_fisica"
        verbose_name_plural = "instalaciones_fisicas"