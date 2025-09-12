from django.db import transaction
from .usuario_service import UsuarioService
from .estudiante_service import EstudianteService
from .docente_service import DocenteService
from .secretaria_service import SecretariaService

class RegistroService:
    @staticmethod
    def validar(email, numeroIdentificacion, codigo_estudiante=None):
        """
        chequeos de preexistencia antes de escribir:
        - email único (Usuario)
        - número de identificación único (Usuario)
        - código estudiante único (Estudiante) si aplica
        """
        if UsuarioService.get_by_email(email):
            return "Ya existe un usuario con ese email"
        if UsuarioService.exists_by_identificacion(numeroIdentificacion):
            return "Ya existe un usuario con ese número de identificación"
        if codigo_estudiante:
            if EstudianteService.get_by_codigo(codigo_estudiante):
                return "El código de estudiante ya está registrado"
        return None

    @staticmethod
    @transaction.atomic  # AQUÍ SÍ: crea Usuario + rol en una sola transacción (todo-o-nada)
    def registrar(payload):
        """
        payload (p. ej., form.cleaned_data):
          comunes: email, password, nombres, apellidos, telefono, numeroIdentificacion, rol
          si rol='estudiante': codigo_estudiante, programa_id
              - usuario.idUsuario -> Estudiante.usuario_id
              - programa_id -> Estudiante.programa_id
          si rol='docente'   : unidad_academica_id
              - usuario.idUsuario -> Docente.usuario_id
              - unidad_academica_id -> Docente.unidadAcademica_id
          si rol='secretaria': facultad_id
              - usuario.idUsuario -> Secretaria.usuario_id
              - facultad_id -> Secretaria.facultad_id (PK real de Facultad en tu modelo = idUsuario)
        """
        # 1) crear usuario base (usa el manager para hashear password)
        usuario = UsuarioService.create({
            "email": payload.get("email"),
            "password": payload.get("password"),
            "nombres": payload.get("nombres"),
            "apellidos": payload.get("apellidos"),
            "telefono": payload.get("telefono"),
            "numeroIdentificacion": payload.get("numeroIdentificacion"),
        })

        # 2) según el rol, crear el registro asociado con los IDs correctos
        rol = payload.get("rol")

        if rol == "estudiante":
            EstudianteService.create(
                usuario_id=usuario.idUsuario,              # FK OneToOne a Usuario
                codigo_estudiante=payload.get("codigo_estudiante"),
                programa_id=payload.get("programa_id")     # FK a Programa (idPrograma)
            )
        elif rol == "docente":
            DocenteService.create(
                usuario_id=usuario.idUsuario,
                unidad_academica_id=payload.get("unidad_academica_id")  # FK a UnidadAcademica (idUnidadAcademica)
            )
        elif rol == "secretaria":
            SecretariaService.create(
                usuario_id=usuario.idUsuario,
                facultad_id=payload.get("facultad_id")     # FK a Facultad (tu PK se llama idUsuario → columna facultad_id)
            )
        else:
            # si llega un rol no contemplado, lanzamos error (la transacción se revierte)
            raise ValueError("Rol no soportado")

        # 3) devolvemos el PK del usuario creado para referencias posteriores
        return usuario.idUsuario
