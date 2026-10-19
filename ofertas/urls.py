from django.urls import path
from . import views

app_name = 'ofertas'

urlpatterns = [
    # Aprendiz
    path('', views.lista_ofertas, name='lista'),
    path('<int:pk>/', views.detalle_oferta, name='detalle'),
    path('<int:pk>/guardar/', views.guardar_oferta, name='guardar'),
    path('<int:pk>/postularme/', views.postularme, name='postularme'),
    path('mis-postulaciones/', views.mis_postulaciones, name='mis_postulaciones'),
    path('postulacion/<int:pk>/actualizar/', views.actualizar_postulacion, name='actualizar_postulacion'),
    path('postulacion/<int:pk>/quitar/', views.quitar_guardada, name='quitar_guardada'),

    # Instructor
    path('gestion/', views.gestion_lista, name='gestion_lista'),
    path('gestion/nueva/', views.gestion_crear, name='gestion_crear'),
    path('gestion/<int:pk>/editar/', views.gestion_editar, name='gestion_editar'),
    path('gestion/<int:pk>/estado/', views.gestion_toggle, name='gestion_toggle'),
    path('gestion/<int:pk>/eliminar/', views.gestion_eliminar, name='gestion_eliminar'),
]