# * File Functions
def path_coordinador_aval(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{instance.organizador.idUsuario}.{ext}"
    return f"events/{instance.evento.idEvento}/organizadores-eventos/{filename}"