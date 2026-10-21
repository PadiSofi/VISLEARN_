from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .services import asegurar_expediente

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def crear_perfil_aprendiz(sender, instance, created, **kwargs):
    if created and instance.is_aprendiz:
        asegurar_expediente(instance)
