from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
from core.models import notificar_instructores
from usuarios.decorators import aprendiz_required, contenido_required
from .forms import ActualizarPostulacionForm, OfertaLaboralForm
from .models import OfertaLaboral, Postulacion

# Create your views here.

# Aprendiz: explorar ofertas
@never_cache
@aprendiz_required
def lista_ofertas(request):
    perfil = request.user.perfil_aprendiz
    vigentes = OfertaLaboral.vigentes()
    ofertas = vigentes

    q = request.GET.get('q', '').strip()
    pais = request.GET.get('pais', '')
    modalidad = request.GET.get('modalidad', '')

    if q:
        ofertas = ofertas.filter(
            Q(titulo__icontains=q) | Q(empresa__icontains=q) |
            Q(tecnologias__icontains=q) | Q(descripcion__icontains=q)
        )
    if pais:
        ofertas = ofertas.filter(pais=pais)
    if modalidad:
        ofertas = ofertas.filter(modalidad=modalidad)

    paginador = Paginator(ofertas, 10)
    page_obj = paginador.get_page(request.GET.get('page'))

    page_obj.object_list = list(page_obj.object_list)
    mapa = dict(Postulacion.objects.filter(perfil=perfil).values_list('oferta_id', 'estado'))
    etiquetas = dict(Postulacion.ESTADO_CHOICES)
    for oferta in page_obj.object_list:
        oferta.estado_postulacion = mapa.get(oferta.pk)
        oferta.estado_postulacion_label = etiquetas.get(oferta.estado_postulacion)

    params = request.GET.copy()
    params.pop('page', None)

    return render(request, 'ofertas/lista.html', {
        'page_obj': page_obj,
        'total_resultados': paginador.count,
        'total_ofertas': vigentes.count(),
        'total_paises': vigentes.values('pais').distinct().count(),
        'paises': vigentes.values_list('pais', flat=True).distinct().order_by('pais'),
        'modalidades': OfertaLaboral.MODALIDAD_CHOICES,
        'q': q,
        'pais_actual': pais,
        'modalidad_actual': modalidad,
        'query_string': params.urlencode(),
    })

@never_cache
@aprendiz_required
def detalle_oferta(request, pk):
    oferta = get_object_or_404(OfertaLaboral, pk=pk)
    postulacion = Postulacion.objects.filter(perfil=request.user.perfil_aprendiz, oferta=oferta).first()
    if not oferta.esta_vigente() and postulacion is None:
        raise Http404
    return render(request, 'ofertas/detalle.html', {'oferta': oferta, 'postulacion': postulacion})

# Aprendiz: guardar, postularse y seguimiento
@require_POST
@aprendiz_required
def guardar_oferta(request, pk):
    oferta = get_object_or_404(OfertaLaboral.vigentes(), pk=pk)
    _, creada = Postulacion.objects.get_or_create(perfil=request.user.perfil_aprendiz, oferta=oferta)
    if creada:
        messages.success(request, 'Oferta guardada. La encuentras en Mis Postulaciones.')
    return redirect('ofertas:detalle', pk=oferta.pk)

@require_POST
@aprendiz_required
def postularme(request, pk):
    oferta = get_object_or_404(OfertaLaboral, pk=pk)
    perfil = request.user.perfil_aprendiz
    postulacion = Postulacion.objects.filter(perfil=perfil, oferta=oferta).first()

    if postulacion and postulacion.estado != 'guardada':
        messages.info(request, 'Ya registraste tu postulación a esta oferta.')
    elif not oferta.esta_vigente():
        messages.error(request, 'Esta convocatoria ya no está vigente.')
    else:
        if postulacion is None:
            postulacion = Postulacion(perfil=perfil, oferta=oferta)
        postulacion.estado = 'postulado'
        postulacion.save()
        notificar_instructores(
            f'{request.user.get_full_name()} se postuló a "{oferta.titulo}" ({oferta.empresa}, {oferta.pais}).',
            reverse('instructor:detalle_aprendiz', args=[perfil.pk]),
        )
        messages.success(request, 'Postulación registrada. Puedes seguirla en Mis Postulaciones.')
    return redirect('ofertas:detalle', pk=oferta.pk)

@require_POST
@aprendiz_required
def quitar_guardada(request, pk):
    postulacion = get_object_or_404(Postulacion, pk=pk, perfil=request.user.perfil_aprendiz)
    if postulacion.estado != 'guardada':
        messages.error(request, 'Solo puedes quitar ofertas guardadas, no postulaciones ya registradas.')
        return redirect('ofertas:mis_postulaciones')

    oferta_pk = postulacion.oferta_id
    volver_a_detalle = request.POST.get('volver') == 'detalle' and postulacion.oferta.esta_vigente()
    postulacion.delete()
    messages.success(request, 'Oferta quitada de tus guardadas.')
    if volver_a_detalle:
        return redirect('ofertas:detalle', pk=oferta_pk)
    return redirect('ofertas:mis_postulaciones')

@never_cache
@aprendiz_required
def mis_postulaciones(request):
    perfil = request.user.perfil_aprendiz
    todas = perfil.postulaciones.select_related('oferta')

    estado = request.GET.get('estado', '')
    validos = dict(Postulacion.ESTADO_CHOICES)
    estado_actual = estado if estado in validos else ''
    postulaciones = todas.filter(estado=estado_actual) if estado_actual else todas

    conteo = {
        fila['estado']: fila['n']
        for fila in todas.order_by().values('estado').annotate(n=Count('id'))
    }
    tabs = [('', 'Todas', sum(conteo.values()))]
    tabs += [(valor, nombre, conteo.get(valor, 0)) for valor, nombre in Postulacion.ESTADO_CHOICES]

    items = [
        (p, ActualizarPostulacionForm(instance=p, auto_id=f'id_%s_{p.pk}'))
        for p in postulaciones
    ]
    return render(request, 'ofertas/mis_postulaciones.html', {
        'items': items,
        'tabs': tabs,
        'estado_actual': estado_actual,
    })

@require_POST
@aprendiz_required
def actualizar_postulacion(request, pk):
    postulacion = get_object_or_404(Postulacion, pk=pk, perfil=request.user.perfil_aprendiz)
    if postulacion.estado == 'guardada':
        messages.error(request, 'Primero usa "Postularme" para registrar tu postulación.')
        return redirect('ofertas:mis_postulaciones')

    estado_anterior = postulacion.estado
    form = ActualizarPostulacionForm(request.POST, instance=postulacion)
    if form.is_valid():
        postulacion = form.save()
        if postulacion.estado != estado_anterior and postulacion.estado in ('en_entrevista', 'aceptada', 'rechazada'):
            notificar_instructores(
                f'{request.user.get_full_name()} actualizó su postulación a "{postulacion.oferta.titulo}": '
                f'{postulacion.get_estado_display()}.',
                reverse('instructor:detalle_aprendiz', args=[postulacion.perfil.pk]),
            )
        messages.success(request, 'Postulación actualizada.')
    else:
        messages.error(request, 'No se pudo actualizar la postulación. Revisa los datos.')
    return redirect('ofertas:mis_postulaciones')

# Instructor: gestión de ofertas
@never_cache
@contenido_required
def gestion_lista(request):
    ofertas = OfertaLaboral.objects.annotate(total_postulaciones=Count('postulaciones'))
    return render(request, 'ofertas/gestion_lista.html', {'ofertas': ofertas})

@never_cache
@contenido_required
def gestion_crear(request):
    if request.method == 'POST':
        form = OfertaLaboralForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Oferta creada correctamente.')
            return redirect('ofertas:gestion_lista')
    else:
        form = OfertaLaboralForm()
    return render(request, 'ofertas/gestion_form.html', {'form': form, 'titulo_pagina': 'Nueva oferta laboral'})

@never_cache
@contenido_required
def gestion_editar(request, pk):
    oferta = get_object_or_404(OfertaLaboral, pk=pk)
    if request.method == 'POST':
        form = OfertaLaboralForm(request.POST, instance=oferta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Oferta actualizada.')
            return redirect('ofertas:gestion_lista')
    else:
        form = OfertaLaboralForm(instance=oferta)
    return render(request, 'ofertas/gestion_form.html', {'form': form, 'titulo_pagina': 'Editar oferta laboral'})

@require_POST
@contenido_required
def gestion_toggle(request, pk):
    oferta = get_object_or_404(OfertaLaboral, pk=pk)
    oferta.activa = not oferta.activa
    oferta.save(update_fields=['activa'])
    messages.success(request, f'Oferta {"activada" if oferta.activa else "desactivada"}.')
    return redirect('ofertas:gestion_lista')

@require_POST
@contenido_required
def gestion_eliminar(request, pk):
    oferta = get_object_or_404(OfertaLaboral, pk=pk)
    if oferta.postulaciones.exists():
        messages.error(request, 'Esta oferta tiene postulaciones de aprendices. Desactívala en vez de eliminarla.')
    else:
        oferta.delete()
        messages.success(request, 'Oferta eliminada.')
    return redirect('ofertas:gestion_lista')
