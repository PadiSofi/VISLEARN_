from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class Usuario(AbstractUser):
    TIPO_DOCUMENTO_CHOICES = [
        ('CC', 'Cédula de ciudadanía'),
        ('CE', 'Cédula de extranjería'),
        ('TI', 'Tarjeta de identidad'),
        ('PPT', 'Permiso por Protección Temporal'),
    ]

    tipo_documento = models.CharField(max_length=3, choices=TIPO_DOCUMENTO_CHOICES)
    numero_documento = models.CharField(max_length=20, unique=True)
    is_aprendiz = models.BooleanField(default=False)
    is_instructor = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['email', 'tipo_documento', 'numero_documento']

    def __str__(self):
        return self.get_full_name() or self.username