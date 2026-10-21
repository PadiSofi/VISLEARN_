from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
from aprendiz.services import asegurar_expediente
from core.models import MensajeContacto, Publicacion, Testimonio
from ofertas.models import OfertaLaboral
from usuarios.decorators import administrador_required
from core.forms import TestimonioForm

# Create your views here.

Usuario = get_user_model()

TABS = {
    'pendientes': Q(solicitud_instructor=True),
    'instructores': Q(is_instructor=True),
    'aprendices': Q(is_aprendiz=True),
    'sin_rol': Q(is_instructor=False, is_aprendiz=False, solicitud_instructor=False),
}
TAB_NOMBRES = [
    ('pendientes', 'Solicitudes'),
    ('instructores', 'Instructores'),
    ('aprendices', 'Aprendices'),
    ('sin_rol', 'Sin rol'),
]

def _correo(usuario, asunto, mensaje):
    if usuario.email:
        send_mail(asunto, mensaje, None, [usuario.email], fail_silently=True)

def _volver(request):
    tab = request.POST.get('tab', 'pendientes')
    if tab not in TABS:
        tab = 'pendientes'
    return redirect(f"{reverse('administracion:usuarios')}?tab={tab}")

@never_cache
@administrador_required
def inicio(request):
    base = Usuario.objects.filter(is_superuser=False)
    return render(request, 'administracion/inicio.html', {
        'pendientes': base.filter(solicitud_instructor=True).count(),
        'instructores': base.filter(is_instructor=True).count(),
        'aprendices': base.filter(is_aprendiz=True).count(),
        'ofertas': OfertaLaboral.vigentes().count(),
        'publicaciones': Publicacion.objects.count(),
        'testimonios': Testimonio.objects.count(),
        'mensajes_nuevos': MensajeContacto.objects.filter(atendido=False).count(),
    })

@never_cache
@administrador_required
def usuarios(request):
    base = Usuario.objects.filter(is_superuser=False)
    conteos = base.aggregate(**{clave: Count('pk', filter=filtro) for clave, filtro in TABS.items()})

    tab = request.GET.get('tab', 'pendientes')
    if tab not in TABS:
        tab = 'pendientes'

    lista = base.filter(TABS[tab]).order_by('-date_joined')
    q = request.GET.get('q', '').strip()
    if q:
        lista = lista.filter(
            Q(first_name__icontains=q) | Q(last_name__icontains=q) |
            Q(numero_documento__icontains=q) | Q(email__icontains=q)
        )

    paginador = Paginator(lista, 15)
    page_obj = paginador.get_page(request.GET.get('page'))
    params = request.GET.copy()
    params.pop('page', None)

    return render(request, 'administracion/usuarios.html', {
        'page_obj': page_obj,
        'tabs': [(clave, nombre, conteos[clave]) for clave, nombre in TAB_NOMBRES],
        'tab': tab,
        'q': q,
        'query_string': params.urlencode(),
    })

@require_POST
@administrador_required
def aprobar_instructor(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk, is_superuser=False, solicitud_instructor=True)
    usuario.is_instructor = True
    usuario.is_aprendiz = False
    usuario.solicitud_instructor = False
    usuario.save(update_fields=['is_instructor', 'is_aprendiz', 'solicitud_instructor'])

    _correo(
        usuario,
        'Tu cuenta de instructor en VisLearn fue aprobada',
        f'Hola {usuario.get_full_name()},\n\n'
        f'Un administrador aprobó tu cuenta de instructor. Ya puedes iniciar sesión con tu '
        f'número de documento aquí: {request.build_absolute_uri(reverse("usuarios:login"))}\n\n'
        f'— Equipo VisLearn',
    )
    messages.success(request, f'{usuario.get_full_name()} ahora es instructor.')
    return _volver(request)

@require_POST
@administrador_required
def rechazar_solicitud(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk, is_superuser=False, solicitud_instructor=True)
    usuario.solicitud_instructor = False
    usuario.save(update_fields=['solicitud_instructor'])

    _correo(
        usuario,
        'Sobre tu solicitud de instructor en VisLearn',
        f'Hola {usuario.get_full_name()},\n\n'
        f'Tu solicitud de cuenta de instructor no fue aprobada. Si crees que es un error, '
        f'puedes escribirnos desde el formulario de contacto de VisLearn.\n\n'
        f'— Equipo VisLearn',
    )
    messages.success(request, f'Solicitud de {usuario.get_full_name()} rechazada. Su cuenta quedó sin rol.')
    return _volver(request)

@require_POST
@administrador_required
def cambiar_rol(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk, is_superuser=False)
    rol = request.POST.get('rol')

    if rol == 'instructor':
        usuario.is_instructor, usuario.is_aprendiz = True, False
    elif rol == 'aprendiz':
        usuario.is_instructor, usuario.is_aprendiz = False, True
    else:
        messages.error(request, 'Rol no válido.')
        return _volver(request)

    usuario.solicitud_instructor = False
    usuario.save(update_fields=['is_instructor', 'is_aprendiz', 'solicitud_instructor'])
    if rol == 'aprendiz':
        asegurar_expediente(usuario)  # perfil, documentos y etapas si no existían

    messages.success(request, f'{usuario.get_full_name()} ahora es {rol}.')
    return _volver(request)

@require_POST
@administrador_required
def toggle_activo(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk, is_superuser=False)
    usuario.is_active = not usuario.is_active
    usuario.save(update_fields=['is_active'])
    estado = 'activada' if usuario.is_active else 'desactivada'
    messages.success(request, f'Cuenta de {usuario.get_full_name()} {estado}.')
    return _volver(request)

# ---------- Testimonios ----------

@never_cache
@administrador_required
def testimonios_lista(request):
    return render(request, 'administracion/testimonios_lista.html', {
        'testimonios': Testimonio.objects.all(),
    })


@never_cache
@administrador_required
def testimonio_crear(request):
    if request.method == 'POST':
        form = TestimonioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Testimonio guardado.')
            return redirect('administracion:testimonios')
    else:
        form = TestimonioForm()
    return render(request, 'administracion/testimonio_form.html', {'form': form, 'titulo_pagina': 'Nuevo testimonio'})


@never_cache
@administrador_required
def testimonio_editar(request, pk):
    testimonio = get_object_or_404(Testimonio, pk=pk)
    if request.method == 'POST':
        form = TestimonioForm(request.POST, instance=testimonio)
        if form.is_valid():
            form.save()
            messages.success(request, 'Testimonio actualizado.')
            return redirect('administracion:testimonios')
    else:
        form = TestimonioForm(instance=testimonio)
    return render(request, 'administracion/testimonio_form.html', {'form': form, 'titulo_pagina': 'Editar testimonio'})


@require_POST
@administrador_required
def testimonio_toggle(request, pk):
    testimonio = get_object_or_404(Testimonio, pk=pk)
    if not testimonio.publicado and not testimonio.autorizacion_confirmada:
        messages.error(request, 'No se puede publicar sin la autorización de la persona. Edita el testimonio y confírmala primero.')
    else:
        testimonio.publicado = not testimonio.publicado
        testimonio.save(update_fields=['publicado'])
        messages.success(request, 'Testimonio publicado.' if testimonio.publicado else 'Testimonio ocultado.')
    return redirect('administracion:testimonios')


@require_POST
@administrador_required
def testimonio_eliminar(request, pk):
    get_object_or_404(Testimonio, pk=pk).delete()
    messages.success(request, 'Testimonio eliminado.')
    return redirect('administracion:testimonios')

@never_cache
@administrador_required
def mensajes_lista(request):
    conteos = MensajeContacto.objects.aggregate(
        pendientes=Count('pk', filter=Q(atendido=False)),
        atendidos=Count('pk', filter=Q(atendido=True)),
        todos=Count('pk'),
    )

    estado = request.GET.get('estado', 'pendientes')
    if estado not in ('pendientes', 'atendidos', 'todos'):
        estado = 'pendientes'

    lista = MensajeContacto.objects.all()
    if estado == 'pendientes':
        lista = lista.filter(atendido=False)
    elif estado == 'atendidos':
        lista = lista.filter(atendido=True)

    q = request.GET.get('q', '').strip()
    if q:
        lista = lista.filter(Q(nombre__icontains=q) | Q(email__icontains=q) | Q(asunto__icontains=q))

    paginador = Paginator(lista, 15)
    page_obj = paginador.get_page(request.GET.get('page'))
    params = request.GET.copy()
    params.pop('page', None)

    return render(request, 'administracion/mensajes.html', {
        'page_obj': page_obj,
        'tabs': [
            ('pendientes', 'Sin atender', conteos['pendientes']),
            ('atendidos', 'Atendidos', conteos['atendidos']),
            ('todos', 'Todos', conteos['todos']),
        ],
        'estado': estado,
        'q': q,
        'query_string': params.urlencode(),
    })

@require_POST
@administrador_required
def mensaje_toggle(request, pk):
    mensaje = get_object_or_404(MensajeContacto, pk=pk)
    mensaje.atendido = not mensaje.atendido
    mensaje.save(update_fields=['atendido'])
    messages.success(request, 'Mensaje marcado como atendido.' if mensaje.atendido else 'Mensaje reabierto.')
    estado = request.POST.get('estado', 'pendientes')
    return redirect(f"{reverse('administracion:mensajes')}?estado={estado if estado in ('pendientes', 'atendidos', 'todos') else 'pendientes'}")

@require_POST
@administrador_required
def mensaje_eliminar(request, pk):
    get_object_or_404(MensajeContacto, pk=pk).delete()
    messages.success(request, 'Mensaje eliminado.')
    return redirect('administracion:mensajes')
