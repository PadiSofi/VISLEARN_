from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
from core.utils import optimizar_imagen

# Create your models here.

class PerfilAprendiz(models.Model):
    ZONA_CHOICES = [('urbana', 'Urbana'), ('rural', 'Rural')]
    ESTRATO_CHOICES = [(str(i), f'Estrato {i}') for i in range(1, 7)]

    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='perfil_aprendiz')
    foto = models.ImageField(upload_to='perfiles/', blank=True, null=True)
    ficha = models.CharField(max_length=20, blank=True)

    lugar_expedicion_documento = models.CharField(max_length=100, blank=True)
    sexo_genero = models.CharField(max_length=100, blank=True)
    correo_personal = models.EmailField(blank=True)
    celular = models.CharField(max_length=20, blank=True)
    telefono_fijo = models.CharField(max_length=20, blank=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    lugar_nacimiento = models.CharField(max_length=100, blank=True)
    direccion_residencia = models.CharField(max_length=200, blank=True)
    barrio = models.CharField(max_length=100, blank=True)
    municipio_departamento = models.CharField(max_length=100, blank=True)

    centro_formacion = models.CharField(max_length=150, blank=True)
    programa_formacion = models.CharField(max_length=150, blank=True)
    nivel_formacion = models.CharField(max_length=100, blank=True)
    ocupacion_perfil_productivo = models.CharField(max_length=150, blank=True)

    zona_residencial = models.CharField(max_length=10, choices=ZONA_CHOICES, blank=True)
    estrato_socioeconomico = models.CharField(max_length=1, choices=ESTRATO_CHOICES, blank=True)
    grupo_sisben = models.CharField(max_length=50, blank=True)
    medio_transporte = models.CharField(max_length=100, blank=True)
    estado_civil = models.CharField(max_length=50, blank=True)
    numero_hijos = models.PositiveSmallIntegerField(default=0)
    eps = models.CharField(max_length=100, blank=True)
    arl = models.CharField(max_length=100, blank=True)
    tipo_sangre = models.CharField(max_length=10, blank=True)
    libreta_militar = models.CharField(max_length=50, blank=True)
    discapacidad_condicion_especial = models.CharField(max_length=150, blank=True)
    multiculturalidad_enfoque_diferencial = models.CharField(max_length=150, blank=True)

    porcentaje_completitud = models.PositiveSmallIntegerField(default=0)

    recibir_notificaciones_email = models.BooleanField(default=True)
    autorizar_tratamiento_datos = models.BooleanField(default=True)
    def __str__(self):
        return f'Perfil de {self.usuario.get_full_name()}'

    pais_destino = models.CharField(max_length=100, blank=True)
    proxima_fecha_importante = models.DateField(blank=True, null=True)
    def porcentaje_avance_proceso(self):
        total = self.etapas.count()
        if total == 0:
            return 0
        completadas = self.etapas.filter(estado='completado').count()
        return round((completadas / total) * 100)

class EstudioAcademico(models.Model):
    perfil = models.ForeignKey(PerfilAprendiz, on_delete=models.CASCADE, related_name='estudios')
    titulo = models.CharField(max_length=150)
    institucion = models.CharField(max_length=150)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    en_curso = models.BooleanField(default=False)

    class Meta:
        ordering = ['-fecha_inicio']

    def __str__(self):
        return f'{self.titulo} - {self.institucion}'


class ExperienciaLaboral(models.Model):
    perfil = models.ForeignKey(PerfilAprendiz, on_delete=models.CASCADE, related_name='experiencias')
    cargo = models.CharField(max_length=150)
    empresa = models.CharField(max_length=150)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    actual = models.BooleanField(default=False)
    descripcion = models.TextField(blank=True)

    class Meta:
        ordering = ['-fecha_inicio']

    def __str__(self):
        return f'{self.cargo} - {self.empresa}'


class Idioma(models.Model):
    NIVEL_CHOICES = [
        ('basico', 'Básico'),
        ('intermedio', 'Intermedio'),
        ('avanzado', 'Avanzado'),
        ('nativo', 'Nativo'),
    ]
    perfil = models.ForeignKey(PerfilAprendiz, on_delete=models.CASCADE, related_name='idiomas')
    idioma = models.CharField(max_length=50)
    nivel = models.CharField(max_length=20, choices=NIVEL_CHOICES)

    def __str__(self):
        return f'{self.idioma} ({self.get_nivel_display()})'

class Documento(models.Model):
    TIPO_CHOICES = [
        ('pasaporte', 'Pasaporte'),
        ('identidad', 'Documento de Identidad'),
        ('carta_aceptacion', 'Carta de Aceptación'),
        ('certificado_academico', 'Certificado Académico'),
        ('fotografia', 'Fotografía Tipo Documento'),
        ('formulario', 'Formulario de Solicitud'),
        ('comprobante_financiero', 'Comprobante de Solvencia Financiera'),
    ]
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_revision', 'En Revisión'),
        ('aprobado', 'Aprobado'),
        ('requiere_correccion', 'Requiere Corrección'),
    ]
    ICONOS = {
        'pasaporte': 'menu_book',
        'identidad': 'badge',
        'carta_aceptacion': 'mail',
        'certificado_academico': 'school',
        'fotografia': 'photo_camera',
        'formulario': 'assignment',
        'comprobante_financiero': 'account_balance',
    }

    perfil = models.ForeignKey(PerfilAprendiz, on_delete=models.CASCADE, related_name='documentos')
    tipo_documento = models.CharField(max_length=30, choices=TIPO_CHOICES)
    archivo = models.FileField(
        upload_to='documentos/%Y/%m/',
        blank=True, null=True,
        validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])],
    )
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    observaciones_instructor = models.TextField(blank=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def icono(self):
        return self.ICONOS.get(self.tipo_documento, 'description')

    def save(self, *args, **kwargs):
        archivo_anterior = None
        if self.pk:
            archivo_anterior = Documento.objects.filter(pk=self.pk).values_list('archivo', flat=True).first()

        # Solo optimiza si se acaba de subir un archivo nuevo
        if self.archivo and not self.archivo._committed:
            self.archivo = optimizar_imagen(self.archivo)

        super().save(*args, **kwargs)

        # Si el archivo cambió, borra el anterior del disco
        if archivo_anterior and archivo_anterior != self.archivo.name:
            self.archivo.storage.delete(archivo_anterior)

    def __str__(self):
        return f'{self.get_tipo_documento_display()} - {self.perfil.usuario}'

class EtapaSeguimiento(models.Model):
    ETAPAS = [
        (1, 'Registro del aprendiz'),
        (2, 'Información personal'),
        (3, 'Selección del destino'),
        (4, 'Revisión de requisitos'),
        (5, 'Recolección de documentos'),
        (6, 'Revisión documental'),
        (7, 'Solicitud de visa'),
        (8, 'Cita consular'),
        (9, 'Espera de respuesta'),
        (10, 'Visa aprobada / proceso finalizado'),
    ]
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('completado', 'Completado'),
        ('requiere_correccion', 'Requiere Corrección'),
    ]

    perfil = models.ForeignKey(PerfilAprendiz, on_delete=models.CASCADE, related_name='etapas')
    numero_etapa = models.PositiveSmallIntegerField(choices=ETAPAS)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    observaciones = models.TextField(blank=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['numero_etapa']
        unique_together = ['perfil', 'numero_etapa']

    def nombre_etapa(self):
        return dict(self.ETAPAS).get(self.numero_etapa)

