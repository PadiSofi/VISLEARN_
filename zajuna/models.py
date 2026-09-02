from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Usuario(models.Model):
    TIPO_DOC_CHOICES = [
        ('TI', 'Tarjeta de Identidad'),
        ('CC', 'Cédula de Ciudadanía'),
        ('CE', 'Cédula de Extranjería'),
        ('PPT', 'Permiso por Protección Temporal'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_documento = models.CharField(max_length=5, choices=TIPO_DOC_CHOICES)
    numero_documento = models.CharField(max_length=20, unique=True)
    programa = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.user.first_name} ({self.numero_documento})"

class Documento(models.Model):
    nombre = models.CharField(max_length=200)
    estado = models.CharField(max_length=50)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class ProcesoVisa(models.Model):
    estado = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.estado

class Cita(models.Model):
    tipo = models.CharField(max_length=200)
    fecha = models.DateField()
    hora = models.TimeField()
    lugar = models.CharField(max_length=200)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.tipo

class Actividad(models.Model):
    descripcion = models.CharField(max_length=300)
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.descripcion