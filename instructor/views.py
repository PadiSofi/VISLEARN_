from django.shortcuts import render
from django.views.decorators.cache import never_cache
from aprendiz.models import PerfilAprendiz
from usuarios.decorators import instructor_required
from django.shortcuts import get_object_or_404, redirect
from aprendiz.models import Documento, EtapaSeguimiento
from .forms import RevisarDocumentoForm, ActualizarEtapaForm
from core.models import notificar
from django.db.models import Q
from aprendiz.models import Documento

# Create your views here.

@never_cache
@instructor_required
def lista_aprendices(request):
    base = PerfilAprendiz.objects.filter(
        usuario__is_aprendiz=True, usuario__is_active=True
    ).select_related('usuario')
    aprendices = base

    query = request.GET.get('q')
    if query:
        aprendices = aprendices.filter(
            Q(usuario__first_name__icontains=query) |
            Q(usuario__last_name__icontains=query) |
            Q(usuario__numero_documento__icontains=query)
        )

    return render(request, 'instructor/aprendices.html', {
        'aprendices': aprendices,
        'query': query or '',
        'total_aprendices': base.count(),
        'documentos_pendientes': Documento.objects.filter(perfil__in=base, estado='en_revision').count(),
        'procesos_completados': sum(1 for p in base if p.porcentaje_avance_proceso() == 100),
    })

@never_cache
@instructor_required
def detalle_aprendiz(request, pk):
    perfil = get_object_or_404(PerfilAprendiz, pk=pk)
    documentos = [(doc, RevisarDocumentoForm(instance=doc)) for doc in perfil.documentos.all()]
    etapas = [(etapa, ActualizarEtapaForm(instance=etapa)) for etapa in perfil.etapas.all()]
    return render(request, 'instructor/detalle_aprendiz.html', {
        'perfil': perfil,
        'documentos': documentos,
        'etapas': etapas,
        'postulaciones': perfil.postulaciones.select_related('oferta'),
    })

@instructor_required
def revisar_documento(request, pk):
    documento = get_object_or_404(Documento, pk=pk)
    if request.method == 'POST':
        form = RevisarDocumentoForm(request.POST, instance=documento)
        if form.is_valid():
            form.save()
            if documento.estado == 'aprobado':
                mensaje = f'Tu documento "{documento.get_tipo_documento_display()}" fue aprobado.'
            elif documento.estado == 'requiere_correccion':
                mensaje = f'Tu documento "{documento.get_tipo_documento_display()}" requiere corrección.'
            else:
                mensaje = f'Tu documento "{documento.get_tipo_documento_display()}" fue actualizado.'
            notificar(documento.perfil.usuario, mensaje, '/aprendiz/seguimiento/')
    return redirect('instructor:detalle_aprendiz', pk=documento.perfil.pk)

@instructor_required
def actualizar_etapa(request, pk):
    etapa = get_object_or_404(EtapaSeguimiento, pk=pk)
    if request.method == 'POST':
        form = ActualizarEtapaForm(request.POST, instance=etapa)
        if form.is_valid():
            form.save()
            notificar(
                etapa.perfil.usuario,
                f'Tu etapa "{etapa.nombre_etapa()}" cambió a {etapa.get_estado_display()}.',
                '/aprendiz/seguimiento/',
            )
    return redirect('instructor:detalle_aprendiz', pk=etapa.perfil.pk)
