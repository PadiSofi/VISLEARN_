from django.contrib import admin
from .models import OfertaLaboral, Postulacion

# Register your models here.

@admin.register(OfertaLaboral)
class OfertaLaboralAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'empresa', 'pais', 'modalidad', 'fecha_cierre', 'activa')
    list_filter = ('activa', 'pais', 'modalidad')
    search_fields = ('titulo', 'empresa', 'tecnologias')

@admin.register(Postulacion)
class PostulacionAdmin(admin.ModelAdmin):
    list_display = ('perfil', 'oferta', 'estado', 'fecha_actualizacion')
    list_filter = ('estado',)