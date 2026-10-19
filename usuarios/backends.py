from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

Usuario = get_user_model()

class NumeroDocumentoBackend(ModelBackend):
    """Autentica usando numero_documento en vez de username."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        numero_documento = username
        try:
            usuario = Usuario.objects.get(numero_documento=numero_documento)
        except Usuario.DoesNotExist:
            return None

        if usuario.check_password(password) and self.user_can_authenticate(usuario):
            return usuario
        return None