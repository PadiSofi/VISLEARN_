from django.db import models
from django.conf import settings
from .utils import optimizar_imagen
from django.utils.text import slugify

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
    instructores = get_user_model().objects.filter(is_instructor=True)
    Notificacion.objects.bulk_create([
        Notificacion(usuario=i, mensaje=mensaje[:255], url=url) for i in instructores
    ])
