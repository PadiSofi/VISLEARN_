from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('servicios/', views.servicios, name='servicios'),
    path('conocenos/', views.conocenos, name='conocenos'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.detalle_publicacion, name='detalle_publicacion'),
    path('contacto/', views.contacto, name='contacto'),
    path('notificacion/<int:pk>/ir/', views.ir_a_notificacion, name='ir_a_notificacion'),
    path('notificaciones/marcar-leidas/', views.marcar_todas_leidas, name='marcar_todas_leidas'),
    path('gestion-blog/', views.blog_gestion, name='blog_gestion'),
    path('gestion-blog/nueva/', views.blog_crear, name='blog_crear'),
    path('gestion-blog/<int:pk>/editar/', views.blog_editar, name='blog_editar'),
    path('gestion-blog/<int:pk>/eliminar/', views.blog_eliminar, name='blog_eliminar'),
    path('privacidad/', views.privacidad, name='privacidad'),
    path('terminos/', views.terminos, name='terminos'),
]
