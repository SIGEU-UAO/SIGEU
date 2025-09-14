# apps/authentication/migrations/0004_create_default_groups.py
from django.db import migrations

def create_default_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")

    estudiantes, _ = Group.objects.get_or_create(name="Estudiantes")
    docentes, _ = Group.objects.get_or_create(name="Docentes")
    secretarias, _ = Group.objects.get_or_create(name="Secretarias")
    administradores, _ = Group.objects.get_or_create(name="Administradores")

    codenames_secretaria = [
        "view_programa",
        "view_unidadacademica",
        "view_facultad",
        "view_estudiante",
        "view_docente",
    ]
    secretaria_perms = list(
        Permission.objects.filter(
            codename__in=codenames_secretaria,
            content_type__app_label="authentication",
        )
    )
    secretarias.permissions.set(secretaria_perms)
    estudiantes.permissions.clear()
    docentes.permissions.clear()
    administradores.permissions.clear()

def delete_default_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.filter(
        name__in=["Estudiantes", "Docentes", "Secretarias", "Administradores"]
    ).delete()

class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0003_alter_facultad_table_alter_unidadacademica_table"),
        ("auth", "0012_alter_user_first_name_max_length"),
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.RunPython(create_default_groups, delete_default_groups),
    ]
