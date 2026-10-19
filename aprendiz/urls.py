from django.urls import path
from . import views

app_name = 'aprendiz'

urlpatterns = [
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/estudio/agregar/', views.agregar_estudio, name='agregar_estudio'),
    path('perfil/estudio/<int:pk>/eliminar/', views.eliminar_estudio, name='eliminar_estudio'),
    path('perfil/experiencia/agregar/', views.agregar_experiencia, name='agregar_experiencia'),
    path('perfil/experiencia/<int:pk>/eliminar/', views.eliminar_experiencia, name='eliminar_experiencia'),
    path('perfil/idioma/agregar/', views.agregar_idioma, name='agregar_idioma'),
    path('perfil/idioma/<int:pk>/eliminar/', views.eliminar_idioma, name='eliminar_idioma'),
    path('seguimiento/', views.seguimiento, name='seguimiento'),
    path('documento/<int:pk>/subir/', views.subir_documento, name='subir_documento'),
]