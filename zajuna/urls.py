from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    # Página principal
    path('', views.inicio, name='inicio'),

    # Información
    path('conocenos/', views.conocenos, name='conocenos'),
    path('servicios/', views.servicios, name='servicios'),
    path('blog/', views.blog, name='blog'),
    path('contacto/', views.contacto, name='contacto'),

    # Usuario
    path('perfil/', views.perfil, name='perfil'),
    path('documentos/', views.documentos, name='documentos'),
    path('seguimiento/', views.seguimiento, name='seguimiento'),

    # Autenticación
    path('iniciosesion/', views.iniciosesion, name='iniciosesion'),
    path('registro/', views.registro, name='registro'),
    path('registroInstructor/', views.registroInstructor, name='registroInstructor'),
    path('logout/', LogoutView.as_view(next_page='inicio'), name='logout'),
]