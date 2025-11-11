from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from apps.core.models import Facultad, Programa, UnidadAcademica

class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El usuario debe tener un email")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    idUsuario = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    numeroIdentificacion = models.CharField(max_length=10, unique=True, verbose_name="Número de Identificación")
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=10, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["numeroIdentificacion", "nombres", "apellidos", "telefono"]

    objects = UsuarioManager()

    @property
    def rol(self):
        if hasattr(self, "estudiante"):
            return "Estudiante"
        elif hasattr(self, "docente"):
            return "Docente"
        elif hasattr(self, "secretaria"):
            return "Secretaria"
        elif self.is_superuser:
            return "Administrador"
        return "Usuario"

    def __str__(self):
        return f"{self.nombres} {self.apellidos} ({self.email})"
    
    class Meta:
        db_table = "usuarios"
    
class Contrasenia(models.Model):
    idContrasenia = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    idUsuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="contrasenias")
    fechaCambio = models.DateTimeField(auto_now_add=True)
    clave = models.CharField(max_length=128)
    es_activa = models.BooleanField(default=True)

    def __str__(self):
        return f"Contraseña de {self.idUsuario.email} ({'Activa' if self.es_activa else 'Inactiva'})"
    
    class Meta:
        db_table = "contrasenias"

class Estudiante(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="estudiante", primary_key=True)
    codigo_estudiante = models.CharField(max_length=7, unique=True)
    programa = models.ForeignKey(Programa, on_delete=models.CASCADE, related_name="estudiantes")

    def __str__(self):
        return f"{self.usuario.nombres} {self.usuario.apellidos} ({self.codigo_estudiante})"
    
    class Meta:
        db_table = "estudiantes"

class Docente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="docente", primary_key=True)
    unidadAcademica = models.ForeignKey(UnidadAcademica, on_delete=models.CASCADE, related_name="docentes")

    def __str__(self):
        return f"{self.usuario.nombres} {self.usuario.apellidos} ({self.unidadAcademica.nombre})"
    
    class Meta:
        db_table = "docentes"

class Secretaria(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="secretaria", primary_key=True)
    facultad = models.ForeignKey(Facultad, on_delete=models.CASCADE, related_name="secretarias")

    def __str__(self):
        return f"{self.usuario.nombres} {self.usuario.apellidos} ({self.facultad.nombre})"
    
    class Meta:
        db_table = "secretarias"
        constraints = [
            models.UniqueConstraint(fields=["facultad"], name="unique_secretaria_por_facultad")
        ]
