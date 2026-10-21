from django.contrib import admin
from .models import MensajeContacto
from .models import MensajeContacto, Publicacion, Testimonio

# Register your models here.

@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):
    list_display = ('asunto', 'nombre', 'email', 'fecha_envio', 'atendido')
    list_filter = ('atendido',)
    search_fields = ('nombre', 'email', 'asunto')

@admin.register(Publicacion)
class PublicacionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'autor', 'fecha_publicacion', 'destacado')
    list_filter = ('categoria', 'destacado')
    prepopulated_fields = {'slug': ('titulo',)}
    search_fields = ('titulo', 'resumen', 'contenido')

@admin.register(Testimonio)
class TestimonioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'rol', 'autorizacion_confirmada', 'publicado', 'fecha_creacion')
    list_filter = ('publicado', 'autorizacion_confirmada')
    search_fields = ('nombre', 'texto')