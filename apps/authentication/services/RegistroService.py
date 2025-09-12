# apps/authentication/services/registro_service.py

from ..models import (
    Usuario,
    Estudiante,
    Docente,
    Secretaria,
    Programa,
    UnidadAcademica,
    Facultad,
)

class RegistroService:
    @staticmethod
    def registrar(data):
        """
        Crea Usuario y, según 'rol', crea Estudiante/Docente/Secretaria.
        Usa .get() para traer objetos relacionados (sin select_related).
        data espera:
          email, password, nombres, apellidos, telefono, numeroIdentificacion, rol
          si rol == 'estudiante' -> codigo_estudiante, programa_id
          si rol == 'docente'    -> unidad_academica_id
          si rol == 'secretaria' -> facultad_id
        """
        # 1) Crear el usuario (usa tu UsuarioManager -> hashea password)
        usuario = Usuario.objects.create_user(
            email=data["email"],
            password=data["password"],
            nombres=data["nombres"],
            apellidos=data["apellidos"],
            telefono=data["telefono"],
            numeroIdentificacion=data["numeroIdentificacion"],
        )

        # 2) Crear la entidad por rol usando .get() 
        rol = data.get("rol")

        try:
            if rol == "estudiante":
                programa = Programa.objects.get(pk=data["programa_id"])  # get -> 404 si no existe
                Estudiante.objects.create(
                    usuario=usuario,
                    codigo_estudiante=data["codigo_estudiante"],
                    programa=programa,  # pasamos el objeto, no *_id
                )

            elif rol == "docente":
                unidad = UnidadAcademica.objects.get(pk=data["unidad_academica_id"])
                Docente.objects.create(
                    usuario=usuario,
                    unidadAcademica=unidad,
                )

            elif rol == "secretaria":
                facultad = Facultad.objects.get(pk=data["facultad_id"])
                Secretaria.objects.create(
                    usuario=usuario,
                    facultad=facultad,
                )

            else:
                # si no se envía rol o no coincide, solo se crea el Usuario
                # (manteniendo la simplicidad que estás pidiendo)
                pass

        except (Programa.DoesNotExist, UnidadAcademica.DoesNotExist, Facultad.DoesNotExist) as fallo:
            # Si la FK no existe, para no dejar al Usuario “huérfano”
            # borramos el usuario recién creado y re-lanzamos un error simple.
            usuario.delete()
            raise ValueError("ID relacionado inválido para el rol seleccionado") from fallo

        return usuario.idUsuario

    @staticmethod
    def listar_usuarios():
        """
        Retorna una lista de dicts con datos básicos de Usuario.
        No necesitamos select_related porque aquí no accedemos a relaciones.
        """
        usuarios = []
        for usuario in Usuario.objects.all().order_by("idUsuario"):
            usuarios.append({
                "id": usuario.idUsuario,
                "email": usuario.email,
                "nombres": usuario.nombres,
                "apellidos": usuario.apellidos,
                "telefono": usuario.telefono,
                "numeroIdentificacion": usuario.numeroIdentificacion,
            })
        return usuarios
