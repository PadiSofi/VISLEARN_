from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .forms import RegistroAprendizForm, LoginNumeroDocumentoForm

# Create your views here.

def registro_aprendiz(request):
    if request.method == 'POST':
        form = RegistroAprendizForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario, backend='usuarios.backends.NumeroDocumentoBackend')
            return redirect('aprendiz:perfil')
    else:
        form = RegistroAprendizForm()
    return render(request, 'autenticacion/registro.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'autenticacion/iniciosesion.html'
    form_class = LoginNumeroDocumentoForm

    def get_success_url(self):
        user = self.request.user
        if user.is_instructor:
            return '/instructor/'
        return '/aprendiz/perfil/'

@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('core:inicio')