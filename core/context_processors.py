def notificaciones(request):
    if request.user.is_authenticated:
        qs = request.user.notificaciones.all()
        return {
            'notificaciones_no_leidas': qs.filter(leida=False).count(),
            'notificaciones_recientes': qs[:8],
        }
    return {}