from django.contrib import admin
from .models import PerfilAprendiz, Documento, EtapaSeguimiento

# Register your models here.

@admin.register(EtapaSeguimiento)
class EtapaSeguimientoAdmin(admin.ModelAdmin):
    list_display = ('perfil', 'numero_etapa', 'estado', 'fecha_actualizacion')
    list_filter = ('estado',)

@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('perfil', 'tipo_documento', 'estado', 'fecha_actualizacion')
    list_filter = ('estado',)