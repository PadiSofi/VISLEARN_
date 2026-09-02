from django.contrib import admin
from .models import Usuario, Documento, ProcesoVisa, Cita, Actividad

# Register your models here.

admin.site.register(Usuario)
admin.site.register(Documento)
admin.site.register(ProcesoVisa)
admin.site.register(Cita)
admin.site.register(Actividad)