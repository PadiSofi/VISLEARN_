from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

# Register your models here.

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Datos VisLearn', {'fields': ('tipo_documento', 'numero_documento', 'is_aprendiz', 'is_instructor')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Datos VisLearn', {'fields': (
            'first_name', 'last_name', 'email',
            'tipo_documento', 'numero_documento',
            'is_aprendiz', 'is_instructor',
        )}),
    )
    list_display = ('numero_documento', 'get_full_name', 'email', 'is_aprendiz', 'is_instructor')
    list_filter = ('is_aprendiz', 'is_instructor')
    search_fields = ('numero_documento', 'first_name', 'last_name', 'email')

