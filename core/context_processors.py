from django.conf import settings

def notificaciones(request):
    if request.user.is_authenticated:
        qs = request.user.notificaciones.all()
        return {
            'notificaciones_no_leidas': qs.filter(leida=False).count(),
            'notificaciones_recientes': qs[:8],
        }
    return {}

def sitio(request):
    return {'sitio': {
        'email': settings.CONTACTO_EMAIL,
        'telefono': settings.CONTACTO_TELEFONO,
        'whatsapp': settings.CONTACTO_WHATSAPP,
        'direccion': settings.CONTACTO_DIRECCION,
        'responsable': settings.RESPONSABLE_DATOS,
    }}