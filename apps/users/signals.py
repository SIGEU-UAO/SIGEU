from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver

@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    """
    Crear grupos y asignar permisos por defecto después de migraciones.
    """

    grupos = {
        "Estudiantes": ["change_estudiante", "view_estudiante"],
        "Docentes": ["change_docente", "view_docente"],
        "Secretarias": ["change_secretaria", "view_secretaria"]
    }

    for nombre_grupo, codenames in grupos.items():
        grupo, _ = Group.objects.get_or_create(name=nombre_grupo)
        permisos = Permission.objects.filter(codename__in=codenames)
        grupo.permissions.set(permisos)
