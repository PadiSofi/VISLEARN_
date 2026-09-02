from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from zajuna.models import Usuario
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def inicio(request):
    return render(request, 'index.html')

def conocenos(request):
    return render(request, 'conocenos.html')

def servicios(request):
    return render(request, 'servicios.html')

def blog(request):
    return render(request, 'blog.html')

def contacto(request):
    return render(request, 'contacto.html')

def iniciosesion(request):
    return render(request, 'iniciosesion.html')

def registroInstructor(request):
    return render(request, 'registroInstructor.html')

def perfil(request):
    return render(request, 'perfil.html')

def documentos(request):
    return render(request, 'documentos.html')

def seguimiento(request):
    return render(request, 'seguimiento.html')

def registro(request):
    if request.method == 'POST':
        nombre = request.POST.get('fullName')
        email = request.POST.get('email')
        password = request.POST.get('password')
        doc_type = request.POST.get('docType')
        doc_number = request.POST.get('docNumber')
        program = request.POST.get('program')

        if User.objects.filter(username=email).exists():
            messages.error(request, "El correo electrónico ya está registrado.")
            return render(request, 'registro.html')

        if Usuario.objects.filter(numero_documento=doc_number).exists():
            messages.error(request, "Ese número de documento ya está registrado.")
            return render(request, 'registro.html')

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=nombre
        )

        Usuario.objects.create(
            user=user,
            tipo_documento=doc_type,
            numero_documento=doc_number,
            programa=program
        )

        user_auth = authenticate(username=email, password=password)
        if user_auth is not None:
            login(request, user_auth)
            messages.success(request, "Registro exitoso. ¡Bienvenido a tu perfil!")
            return redirect('perfil')

    return render(request, 'registro.html')

def iniciosesion(request):
    if request.method == 'POST':
        doc_type = request.POST.get('docType')
        doc_number = request.POST.get('docNumber')
        password = request.POST.get('password')

        # Buscar el perfil correspondiente al número de documento
        perfil = Usuario.objects.filter(numero_documento=doc_number, tipo_documento=doc_type).first()

        if perfil:
            # Autenticar con el username del User asociado
            user = authenticate(request, username=perfil.user.username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"¡Bienvenido de nuevo, {user.first_name}!")
                return redirect('perfil')  # Redirección automática al perfil
            else:
                messages.error(request, "Contraseña incorrecta.")
        else:
            messages.error(request, "No existe un usuario registrado con ese documento.")

    return render(request, 'iniciosesion.html')

@login_required(login_url='iniciosesion')
def perfil(request):
    # Obtener el perfil asociado al usuario autenticado
    perfil_usuario = Usuario.objects.filter(user=request.user).first()
    return render(request, 'perfil.html', {'perfil': perfil_usuario})

@login_required(login_url='iniciosesion')
def documentos(request):
    return render(request, 'documentos.html')

@login_required(login_url='iniciosesion')
def seguimiento(request):
    return render(request, 'seguimiento.html')