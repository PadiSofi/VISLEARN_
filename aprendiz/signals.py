from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import PerfilAprendiz, Documento, EtapaSeguimiento

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def crear_perfil_aprendiz(sender, instance, created, **kwargs):
    if created and instance.is_aprendiz:
        perfil = PerfilAprendiz.objects.create(usuario=instance)
        for tipo, _ in Documento.TIPO_CHOICES:
            Documento.objects.create(perfil=perfil, tipo_documento=tipo)
        for numero, _ in EtapaSeguimiento.ETAPAS:
            estado_inicial = 'completado' if numero == 1 else 'pendiente'
            EtapaSeguimiento.objects.create(perfil=perfil, numero_etapa=numero, estado=estado_inicial)

