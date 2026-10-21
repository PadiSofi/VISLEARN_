from django.urls import path
from . import views

app_name = 'administracion'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('usuarios/', views.usuarios, name='usuarios'),
    path('usuarios/<int:pk>/aprobar/', views.aprobar_instructor, name='aprobar_instructor'),
    path('usuarios/<int:pk>/rechazar/', views.rechazar_solicitud, name='rechazar_solicitud'),
    path('usuarios/<int:pk>/rol/', views.cambiar_rol, name='cambiar_rol'),
    path('usuarios/<int:pk>/activo/', views.toggle_activo, name='toggle_activo'),
    path('testimonios/', views.testimonios_lista, name='testimonios'),
    path('testimonios/nuevo/', views.testimonio_crear, name='testimonio_crear'),
    path('testimonios/<int:pk>/editar/', views.testimonio_editar, name='testimonio_editar'),
    path('testimonios/<int:pk>/publicar/', views.testimonio_toggle, name='testimonio_toggle'),
    path('testimonios/<int:pk>/eliminar/', views.testimonio_eliminar, name='testimonio_eliminar'),
    path('mensajes/', views.mensajes_lista, name='mensajes'),
    path('mensajes/<int:pk>/atendido/', views.mensaje_toggle, name='mensaje_toggle'),
    path('mensajes/<int:pk>/eliminar/', views.mensaje_eliminar, name='mensaje_eliminar'),
]