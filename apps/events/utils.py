# * File Functions
def path_coordinador_aval(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{instance.organizador.id_usuario}.{ext}"
    return f"events/{instance.evento.id_evento}/organizadores-eventos/{filename}"

def path_organizacion_certificado(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{instance.organizacion.id_organizacion}.{ext}"
    return f"events/{instance.evento.id_evento}/organizaciones-invitadas/{filename}"

def path_acta(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{instance.evento.id_evento}.{ext}"
    return f"events/{instance.evento.id_evento}/Acta-Evento.{ext}"