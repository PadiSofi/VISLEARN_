from .models import PerfilAprendiz, Documento, EtapaSeguimiento


def asegurar_expediente(usuario):
    """Crea (si faltan) el perfil, los documentos y las etapas de un aprendiz."""
    perfil, _ = PerfilAprendiz.objects.get_or_create(usuario=usuario)
    for tipo, _nombre in Documento.TIPO_CHOICES:
        Documento.objects.get_or_create(perfil=perfil, tipo_documento=tipo)
    for numero, _nombre in EtapaSeguimiento.ETAPAS:
        EtapaSeguimiento.objects.get_or_create(
            perfil=perfil,
            numero_etapa=numero,
            defaults={'estado': 'completado' if numero == 1 else 'pendiente'},
        )
    return perfil
