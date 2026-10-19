from django.db import models
from django.db.models import Q
from django.utils import timezone

# Create your models here.

class OfertaLaboral(models.Model):
    MODALIDAD_CHOICES = [
        ('presencial', 'Presencial'),
        ('hibrido', 'Híbrido'),
        ('remoto', 'Remoto'),
    ]

    titulo = models.CharField(max_length=200)
    empresa = models.CharField(max_length=150)
    pais = models.CharField(max_length=80)
    ciudad = models.CharField(max_length=100, blank=True)
    modalidad = models.CharField(max_length=15, choices=MODALIDAD_CHOICES)
    salario = models.CharField(max_length=120, blank=True, help_text='Texto libre. Ej: 3.800 - 4.400 EUR / mes')
    descripcion = models.TextField()
    requisitos = models.TextField(help_text='Un requisito por línea.')
    beneficios = models.TextField(blank=True, help_text='Un beneficio por línea.')
    tecnologias = models.CharField(max_length=250, blank=True, help_text='Separadas por coma. Ej: Python, Django, PostgreSQL')
    idioma_requerido = models.CharField(max_length=100, blank=True)
    tipo_visa = models.CharField(max_length=120, blank=True, help_text='Visa o permiso de trabajo que aplica o patrocina la empresa.')
    enlace_externo = models.URLField(blank=True, help_text='Enlace a la convocatoria original de la empresa.')
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    fecha_cierre = models.DateField(blank=True, null=True)
    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ['-fecha_publicacion']
        verbose_name = 'Oferta laboral'
        verbose_name_plural = 'Ofertas laborales'

    def __str__(self):
        return f'{self.titulo} - {self.empresa}'

    @classmethod
    def vigentes(cls):
        hoy = timezone.localdate()
        return cls.objects.filter(activa=True).filter(Q(fecha_cierre__isnull=True) | Q(fecha_cierre__gte=hoy))

    def esta_vigente(self):
        return self.activa and (self.fecha_cierre is None or self.fecha_cierre >= timezone.localdate())

    @staticmethod
    def _lineas(texto):
        return [linea.strip() for linea in texto.splitlines() if linea.strip()]

    def lista_requisitos(self):
        return self._lineas(self.requisitos)

    def lista_beneficios(self):
        return self._lineas(self.beneficios)

    def lista_tecnologias(self):
        return [t.strip() for t in self.tecnologias.split(',') if t.strip()]


class Postulacion(models.Model):
    ESTADO_CHOICES = [
        ('guardada', 'Guardada'),
        ('postulado', 'Postulado'),
        ('en_entrevista', 'En entrevista'),
        ('aceptada', 'Aceptada'),
        ('rechazada', 'Rechazada'),
    ]

    perfil = models.ForeignKey('aprendiz.PerfilAprendiz', on_delete=models.CASCADE, related_name='postulaciones')
    oferta = models.ForeignKey(OfertaLaboral, on_delete=models.PROTECT, related_name='postulaciones')
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='guardada')
    notas = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha_actualizacion']
        constraints = [
            models.UniqueConstraint(fields=['perfil', 'oferta'], name='postulacion_unica_por_oferta'),
        ]

    def __str__(self):
        return f'{self.perfil.usuario} → {self.oferta} ({self.get_estado_display()})'
