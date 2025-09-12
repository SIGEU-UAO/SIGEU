from django.http import JsonResponse
from .services.registro_service import RegistroService
from .services.usuario_service import UsuarioService

def usuarios_listar(request):
    # 1) Pedimos al service la lista de usuarios (la view NO toca el ORM).
    usuarios = UsuarioService.list()

    # 2) Preparar el arreglo de salida (convertimos objetos a dicts simples).
    resultado = []
    for usuario in usuarios:  # nombre completo en el for (usuario)
        resultado.append({
            "id": usuario.idUsuario,     # PK del Usuario según tu modelo
            "email": usuario.email,
            "nombres": usuario.nombres,
            "apellidos": usuario.apellidos,
            "telefono": usuario.telefono,
        })

    # 3) Devolver JSON de la lista (safe=False porque devolvemos un array, no un dict).
    return JsonResponse(resultado, safe=False)


def formulario_registro(request):
    if request.method == "POST":
        rol = request.POST.get("rol")
        registros = {
            "email": request.POST.get("email"),
            "password": request.POST.get("password1"),
            "nombres": request.POST.get("nombre"),
            "apellidos": request.POST.get("apellido"),
            "telefono": request.POST.get("telefono"),
            "numeroIdentificacion": request.POST.get("documento"),
            "rol": rol,
        }
        if rol == "estudiante":
            registros["codigo_estudiante"] = request.POST.get("codigo_estudiante")
            registros["programa_id"] = request.POST.get("programa")
        elif rol == "docente":
            registros["unidad_academica_id"] = request.POST.get("unidadAcademica")
        elif rol == "secretaria":
            registros["facultad_id"] = request.POST.get("facultad")

        usuario_id = RegistroService.registrar(registros)
        return JsonResponse({"id": usuario_id, "message": "registro creado"}, status=201)

    return JsonResponse({"error": "usa POST"}, status=405)
