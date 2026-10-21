from django.db import models
from django.conf import settings
from .utils import optimizar_imagen
from django.utils.text import slugify
from django.core.exceptions import ValidationError

# Create your models here.

class MensajeContacto(models.Model):
    nombre = models.CharField(max_length=120)
    email = models.EmailField()
    asunto = models.CharField(max_length=150)
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    atendido = models.BooleanField(default=False)

    class Meta:
        ordering = ['-fecha_envio']

    def __str__(self):
        return f'{self.asunto} - {self.nombre}'

class Publicacion(models.Model):
    CATEGORIA_CHOICES = [
        ('visa', 'Guías de Visa'),
        ('testimonios', 'Testimonios'),
        ('oportunidades', 'Oportunidades'),
        ('consejos', 'Consejos'),
    ]

    CATEGORIA_DESCRIPCION = {
        'visa': 'Pasos, requisitos y recomendaciones para tramitar tu visa.',
        'testimonios': 'Historias de quienes ya vivieron el proceso.',
        'oportunidades': 'Programas y ofertas para estudiar o trabajar fuera del país.',
        'consejos': 'Ideas prácticas para preparar tu proceso.',
    }
    CATEGORIA_ICONO = {
        'visa': 'menu_book',
        'testimonios': 'forum',
        'oportunidades': 'work',
        'consejos': 'lightbulb',
    }

    def tiempo_lectura(self):
        return max(1, round(len(self.contenido.split()) / 200))

    def icono_categoria(self):
        return self.CATEGORIA_ICONO.get(self.categoria, 'article')

    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    resumen = models.CharField(max_length=300)
    contenido = models.TextField()
    imagen = models.ImageField(upload_to='blog/', blank=True, null=True)
    autor = models.CharField(max_length=100, default='Equipo VisLearn')
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    destacado = models.BooleanField(default=False)

    class Meta:
        ordering = ['-fecha_publicacion']

    def _generar_slug(self):
        base = slugify(self.titulo)[:200] or 'publicacion'
        slug, n = base, 2
        while Publicacion.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f'{base}-{n}'
            n += 1
        return slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generar_slug()

        imagen_anterior = None
        if self.pk:
            imagen_anterior = Publicacion.objects.filter(pk=self.pk).values_list('imagen', flat=True).first()

        if self.imagen and not self.imagen._committed:
            self.imagen = optimizar_imagen(self.imagen, max_lado=1400)

        super().save(*args, **kwargs)

        if imagen_anterior and imagen_anterior != self.imagen.name:
            self.imagen.storage.delete(imagen_anterior)

    def __str__(self):
        return self.titulo

class Notificacion(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notificaciones')
    mensaje = models.CharField(max_length=255)
    url = models.CharField(max_length=255, blank=True)
    leida = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return self.mensaje


def notificar(usuario, mensaje, url=''):
    Notificacion.objects.create(usuario=usuario, mensaje=mensaje, url=url)

def notificar_instructores(mensaje, url=''):
    from django.contrib.auth import get_user_model
    instructores = get_user_model().objects.filter(is_instructor=True, is_active=True)
    Notificacion.objects.bulk_create([
        Notificacion(usuario=i, mensaje=mensaje[:255], url=url) for i in instructores
    ])

def notificar_administradores(mensaje, url=''):
    from django.contrib.auth import get_user_model
    admins = get_user_model().objects.filter(is_superuser=True, is_active=True)
    Notificacion.objects.bulk_create([
        Notificacion(usuario=a, mensaje=mensaje[:255], url=url) for a in admins
    ])

class Testimonio(models.Model):
    nombre = models.CharField(max_length=100)
    rol = models.CharField(max_length=120, help_text='Ej: Desarrollador de software, Berlín')
    texto = models.TextField(max_length=400)
    autorizacion_confirmada = models.BooleanField(
        default=False,
        help_text='Marca esta casilla solo si la persona autorizó por escrito publicar su nombre y su testimonio.',
    )
    publicado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Testimonio'
        verbose_name_plural = 'Testimonios'

    def __str__(self):
        return f'{self.nombre} - {self.rol}'

    def clean(self):
        if self.publicado and not self.autorizacion_confirmada:
            raise ValidationError('No se puede publicar un testimonio sin la autorización de la persona.')
