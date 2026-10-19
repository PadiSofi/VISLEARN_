from django.urls import path
from . import views

app_name = 'instructor'

urlpatterns = [
    path('', views.lista_aprendices, name='lista_aprendices'),
    path('aprendiz/<int:pk>/', views.detalle_aprendiz, name='detalle_aprendiz'),
    path('documento/<int:pk>/revisar/', views.revisar_documento, name='revisar_documento'),
    path('etapa/<int:pk>/actualizar/', views.actualizar_etapa, name='actualizar_etapa'),
]