from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ContactoForm, PublicacionForm
from .models import Publicacion
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import Notificacion, Testimonio
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
from usuarios.decorators import contenido_required
from ofertas.models import OfertaLaboral
from django.urls import reverse
from .models import notificar_administradores

# Create your views here.

def inicio(request):
    vigentes = OfertaLaboral.vigentes()
    stats = {
        'ofertas': vigentes.count(),
        'paises': vigentes.values('pais').distinct().count(),
        'articulos': Publicacion.objects.count(),
    }
    testimonios = Testimonio.objects.filter(publicado=True, autorizacion_confirmada=True)[:3]
    return render(request, 'index.html', {'stats': stats, 'testimonios': testimonios})

def servicios(request):
    return render(request, 'servicios.html')

def conocenos(request):
    return render(request, 'conocenos.html')

def blog(request):
    categorias_validas = dict(Publicacion.CATEGORIA_CHOICES)
    categoria = request.GET.get('categoria')
    if categoria not in categorias_validas:
        categoria = None

    publicaciones = Publicacion.objects.all()
    destacada = None
    encabezado = None

    if categoria:
        publicaciones = publicaciones.filter(categoria=categoria)
        encabezado = {
            'nombre': categorias_validas[categoria],
            'descripcion': Publicacion.CATEGORIA_DESCRIPCION.get(categoria, ''),
            'icono': Publicacion.CATEGORIA_ICONO.get(categoria, 'article'),
            'total': publicaciones.count(),
        }
    else:
        destacada = Publicacion.objects.filter(destacado=True).first()
        if destacada:
            publicaciones = publicaciones.exclude(pk=destacada.pk)

    return render(request, 'blog.html', {
        'publicaciones': publicaciones,
        'destacada': destacada,
        'encabezado': encabezado,
        'categorias': Publicacion.CATEGORIA_CHOICES,
        'categoria_actual': categoria,
    })


def detalle_publicacion(request, slug):
    publicacion = get_object_or_404(Publicacion, slug=slug)

    relacionadas = list(
        Publicacion.objects.filter(categoria=publicacion.categoria).exclude(pk=publicacion.pk)[:3]
    )
    if len(relacionadas) < 3:
        excluir = [r.pk for r in relacionadas] + [publicacion.pk]
        relacionadas += list(Publicacion.objects.exclude(pk__in=excluir)[:3 - len(relacionadas)])

    return render(request, 'blog_detalle.html', {
        'publicacion': publicacion,
        'relacionadas': relacionadas,
    })

def contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            mensaje = form.save()
            notificar_administradores(
                f'Nuevo mensaje de contacto de {mensaje.nombre}: {mensaje.asunto}',
                reverse('administracion:mensajes') + '?estado=pendientes',
            )
            send_mail(
                subject=f'[VisLearn Contacto] {mensaje.asunto}',
                message=f'De: {mensaje.nombre} ({mensaje.email})\n\n{mensaje.mensaje}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=True,
            )
            messages.success(request, '¡Gracias! Tu mensaje fue enviado correctamente.')
            return redirect('core:contacto')
    else:
        form = ContactoForm()
    return render(request, 'contacto.html', {'form': form})

def proximamente(request):
    return render(request, 'proximamente.html')

@login_required
def ir_a_notificacion(request, pk):
    notificacion = get_object_or_404(Notificacion, pk=pk, usuario=request.user)
    notificacion.leida = True
    notificacion.save()
    return redirect(notificacion.url or 'core:inicio')

@login_required
def marcar_todas_leidas(request):
    request.user.notificaciones.filter(leida=False).update(leida=True)
    return redirect(request.META.get('HTTP_REFERER', '/'))

@never_cache
@contenido_required
def blog_gestion(request):
    return render(request, 'blog_gestion.html', {'publicaciones': Publicacion.objects.all()})

@never_cache
@contenido_required
def blog_crear(request):
    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Publicación creada correctamente.')
            return redirect('core:blog_gestion')
    else:
        form = PublicacionForm(initial={'autor': request.user.get_full_name()})
    return render(request, 'blog_gestion_form.html', {'form': form, 'titulo_pagina': 'Nueva publicación'})

@never_cache
@contenido_required
def blog_editar(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk)
    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES, instance=publicacion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Publicación actualizada.')
            return redirect('core:blog_gestion')
    else:
        form = PublicacionForm(instance=publicacion)
    return render(request, 'blog_gestion_form.html', {'form': form, 'titulo_pagina': 'Editar publicación'})

@require_POST
@contenido_required
def blog_eliminar(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk)
    if publicacion.imagen:
        publicacion.imagen.delete(save=False)  # borra también el archivo del disco
    publicacion.delete()
    messages.success(request, 'Publicación eliminada.')
    return redirect('core:blog_gestion')

def privacidad(request):
    return render(request, 'privacidad.html')

def terminos(request):
    return render(request, 'terminos.html')
