from django.db import IntegrityError
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import check_password
from django.conf import settings
from .models import *

# Límite de historial de contraseñas (por defecto 3 si no está configurado)
PASSWORD_HISTORY_LIMIT = getattr(settings, 'PASSWORD_HISTORY_LIMIT', 3)


def validate_new_password(user, new_password):
    """
    Valida que la nueva contraseña no sea igual a la actual ni a las últimas N usadas por el usuario.
    """
    if not new_password:
        raise ValueError("La nueva contraseña es requerida.")

    # Comparar con la actual
    if check_password(new_password, user.password):
        raise ValueError("No puede ser igual a la actual.")

    # Comparar con historial (últimas N)
    historial = (
        Contrasenia.objects
        .filter(idUsuario=user)
        .order_by('-fechaCambio')[:PASSWORD_HISTORY_LIMIT]
    )
    for h in historial:
        if check_password(new_password, h.clave):
            raise ValueError("Ya la usaste antes.")

    return True


def save_password_history(user):
    """
    Guarda el hash de la contraseña actual del usuario en el historial y mantiene sólo las últimas N.
    """
    # Marcar anteriores activas como inactivas
    Contrasenia.objects.filter(idUsuario=user, es_activa=True).update(es_activa=False)

    # Registrar nueva contraseña (hash actual)
    Contrasenia.objects.create(idUsuario=user, clave=user.password, es_activa=True)

    # Limitar historial a N entradas más recientes
    ids_a_conservar = list(
        Contrasenia.objects
        .filter(idUsuario=user)
        .order_by('-fechaCambio')
        .values_list('idContrasenia', flat=True)[:PASSWORD_HISTORY_LIMIT]
    )
    if ids_a_conservar:
        Contrasenia.objects.filter(idUsuario=user).exclude(idContrasenia__in=ids_a_conservar).delete()


class UserService:
    @staticmethod
    def registrar(data):
     
        rol = data.get("rol")

        try:
            usuario = Usuario.objects.create_user(
                email=data["email"],
                password=data["password"],
                nombres=data["nombres"],
                apellidos=data["apellidos"],
                telefono=data["telefono"],
                numeroIdentificacion=data["numeroIdentificacion"],
            )
        except IntegrityError as e:
            s = str(e).lower()
            if "email" in s:
                raise ValueError("El correo electrónico ya está registrado.") from e
            if "numeroidentificacion" in s or "numero_identificacion" in s:
                raise ValueError("El documento de identidad ya está registrado.") from e
            raise ValueError("Datos duplicados en el usuario.") from e
        
        # --- Guardar la contraseña inicial en el historial ---
        Contrasenia.objects.create(
            idUsuario=usuario,
            clave=usuario.password,  # hash generado por set_password
            es_activa=True,
        )

        # --- Crear el registro según el rol; si falla, limpiar al usuario ---
        try:
            if rol == "estudiante":
                programa = Programa.objects.get(pk=data["programa_id"])
                estudiantes = Group.objects.get(name="Estudiantes")      
                Estudiante.objects.create(usuario=usuario, codigo_estudiante=data["codigo_estudiante"], programa=programa)
                usuario.groups.add(estudiantes)

            elif rol == "docente":
                docentes = Group.objects.get(name="Docentes") 
                unidad = UnidadAcademica.objects.get(pk=data["unidad_academica_id"])
                Docente.objects.create(usuario=usuario, unidadAcademica=unidad)
                usuario.groups.add(docentes) 

            elif rol == "secretaria":
                secretarias = Group.objects.get(name="Secretarias") 
                facultad = Facultad.objects.get(pk=data["facultad_id"])
                Secretaria.objects.create(usuario=usuario, facultad=facultad)
                usuario.groups.add(secretarias)

        except (Programa.DoesNotExist, UnidadAcademica.DoesNotExist, Facultad.DoesNotExist) as e:
            usuario.delete()
            raise ValueError("ID relacionado inválido para el rol seleccionado.") from e

        except IntegrityError as e:
            usuario.delete()
            s = str(e).lower()
            if "codigo_estudiante" in s or "codigo" in s:
                raise ValueError("El código de estudiante ya existe.") from e
            raise ValueError("Datos duplicados para el registro del rol.") from e

        except Exception as e:
            usuario.delete()
            raise

        return usuario.idUsuario

    @staticmethod
    def cambiar_password(user, new_password):
        """
        Cambia la contraseña del usuario validando el historial.
        """
        validate_new_password(user, new_password)
        user.set_password(new_password)
        user.save()
        save_password_history(user)
        return True
    
