from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

app_name = 'usuarios'

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('cuenta-pendiente/', views.pendiente, name='pendiente'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='autenticacion/password_reset.html',
        email_template_name='autenticacion/password_reset_email.html',
        subject_template_name='autenticacion/password_reset_subject.txt',
        success_url=reverse_lazy('usuarios:password_reset_done'),
    ), name='password_reset'),
    
    path('password-reset/hecho/', auth_views.PasswordResetDoneView.as_view(
        template_name='autenticacion/password_reset_done.html'
    ), name='password_reset_done'),
    
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='autenticacion/password_reset_confirm.html',
        success_url=reverse_lazy('usuarios:password_reset_complete'),
    ), name='password_reset_confirm'),
    
    path('password-reset-completo/', auth_views.PasswordResetCompleteView.as_view(
        template_name='autenticacion/password_reset_complete.html'
    ), name='password_reset_complete'),
]
