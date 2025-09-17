from django.db import IntegrityError
from django.contrib.auth.models import Group
from ..models import *

class RegistroService:
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
        )

        # --- Crear el registro según el rol; si falla, limpiar al usuario ---
        try:
            if rol == "estudiante":
                programa = Programa.objects.get(pk=data["programa_id"])
                estudiantes = Group.objects.get(name="Estudiantes")      
                Estudiante.objects.create(
                    usuario=usuario,
                    codigo_estudiante=data["codigo_estudiante"],
                    programa=programa,
                )
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
    
