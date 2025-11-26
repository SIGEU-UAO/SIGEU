class EventoSerializer:
    """Converts Event instances into dictionaries ready for JSONResponse."""

    @staticmethod
    def to_dict(evento):
        organizadores = []
        for o in evento.organizadores_asignados.all():
            u = o.organizador
            organizadores.append({
                "nombre": f"{getattr(u, 'nombres', '')} {getattr(u, 'apellidos', '')}".strip(),
                "rol_organizador": getattr(o, "get_tipo_display", lambda: o.tipo)()
            })

        organizaciones = []
        for oi in evento.organizaciones_invitadas.all():
            org = oi.organizacion
            organizaciones.append({
                "nombre": getattr(org, "nombre", None),
                "nit": getattr(org, "nit", None)
            })

        instalaciones = [
            getattr(a.instalacion, "ubicacion", str(a.instalacion))
            for a in evento.instalaciones_asignadas.all()
        ]

        return {
            "id_evento": evento.id_evento,
            "nombre": evento.nombre,
            "tipo": evento.tipo,
            "descripcion": evento.descripcion,
            "fecha_inicio": evento.fecha_inicio.isoformat() if evento.fecha_inicio else None,
            "fecha_fin": evento.fecha_fin.isoformat() if evento.fecha_fin else None,
            "hora_inicio": evento.hora_inicio.isoformat() if evento.hora_inicio else None,
            "hora_fin": evento.hora_fin.isoformat() if evento.hora_fin else None,
            "estado": evento.estado,
            "instalaciones": instalaciones,
            "organizadores": organizadores,
            "organizaciones_invitadas": organizaciones,
        }

    @staticmethod
    def serialize_page(page_obj):
        """Serializa una página completa de eventos paginados."""
        results = [EventoSerializer.to_dict(e) for e in page_obj.object_list]
        return {
            "count": page_obj.paginator.count,
            "num_pages": page_obj.paginator.num_pages,
            "current_page": page_obj.number,
            "results": results,
        }