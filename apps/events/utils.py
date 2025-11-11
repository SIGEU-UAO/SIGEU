# * File Functions
def path_coordinador_aval(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{instance.organizador.idUsuario}.{ext}"
    return f"events/{instance.evento.idEvento}/organizadores-eventos/{filename}"

def path_organizacion_certificado(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{instance.organizacion.idOrganizacion}.{ext}"
    return f"events/{instance.evento.idEvento}/organizaciones-invitadas/{filename}"

def path_acta(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{instance.evento.idEvento}.{ext}"
    return f"events/{instance.evento.idEvento}/Acta-Evento.{ext}"