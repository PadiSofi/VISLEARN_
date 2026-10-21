from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse
from core.models import notificar_administradores
from .forms import LoginNumeroDocumentoForm, RegistroUsuarioForm

def registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()

            if usuario.solicitud_instructor:
                url_solicitudes = reverse('administracion:usuarios') + '?tab=pendientes'
                notificar_administradores(
                    f'{usuario.get_full_name()} solicitó una cuenta de instructor.',
                    url_solicitudes,
                )
                send_mail(
                    subject='[VisLearn] Nueva solicitud de instructor',
                    message=(
                        f'{usuario.get_full_name()} (documento {usuario.numero_documento}) '
                        f'solicitó una cuenta de instructor.\n\n'
                        f'Revísala aquí: {request.build_absolute_uri(url_solicitudes)}'
                    ),
                    from_email=None,
                    recipient_list=[settings.ADMIN_EMAIL],
                    fail_silently=True,
                )

            login(request, usuario, backend='usuarios.backends.NumeroDocumentoBackend')
            if usuario.solicitud_instructor:
                return redirect('usuarios:pendiente')
            return redirect('aprendiz:perfil')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'autenticacion/registro.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'autenticacion/iniciosesion.html'
    form_class = LoginNumeroDocumentoForm

    def get_success_url(self):
        user = self.request.user
        if user.is_superuser:
            return reverse('administracion:inicio')
        if user.is_instructor:
            return reverse('instructor:lista_aprendices')
        if user.is_aprendiz:
            return reverse('aprendiz:perfil')
        return reverse('usuarios:pendiente')

@login_required
def pendiente(request):
    user = request.user
    # Si ya tiene rol (por ejemplo, lo acaban de aprobar), lo enviamos a su panel
    if user.is_superuser:
        return redirect('administracion:inicio')
    if user.is_instructor:
        return redirect('instructor:lista_aprendices')
    if user.is_aprendiz:
        return redirect('aprendiz:perfil')
    return render(request, 'autenticacion/pendiente.html')

@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('core:inicio')