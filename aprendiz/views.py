from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from usuarios.decorators import aprendiz_required
from .forms import InformacionPersonalForm, CaracterizacionSocioeconomicaForm
from django.shortcuts import get_object_or_404
from .models import EstudioAcademico, ExperienciaLaboral, Idioma
from .forms import EstudioAcademicoForm, ExperienciaLaboralForm, IdiomaForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import PrivacidadForm
from .forms import SubirDocumentoForm
from .models import Documento
from django.contrib.auth import get_user_model
from core.models import notificar

# Create your views here.

@never_cache
@aprendiz_required
def perfil(request):
    perfil = request.user.perfil_aprendiz

    if request.method == 'POST':
        form_id = request.POST.get('form_id')

        if form_id == 'caracterizacion':
            form_caracterizacion = CaracterizacionSocioeconomicaForm(request.POST, instance=perfil)
            if form_caracterizacion.is_valid():
                form_caracterizacion.save()
                return redirect('aprendiz:perfil')
            form_personal = InformacionPersonalForm(instance=perfil)
            form_password = PasswordChangeForm(request.user)
            form_privacidad = PrivacidadForm(instance=perfil)

        elif form_id == 'password':
            form_password = PasswordChangeForm(request.user, request.POST)
            if form_password.is_valid():
                usuario = form_password.save()
                update_session_auth_hash(request, usuario)  # evita que cierre sesión al cambiar la clave
                return redirect('aprendiz:perfil')
            form_personal = InformacionPersonalForm(instance=perfil)
            form_caracterizacion = CaracterizacionSocioeconomicaForm(instance=perfil)
            form_privacidad = PrivacidadForm(instance=perfil)

        elif form_id == 'privacidad':
            form_privacidad = PrivacidadForm(request.POST, instance=perfil)
            if form_privacidad.is_valid():
                form_privacidad.save()
                return redirect('aprendiz:perfil')
            form_personal = InformacionPersonalForm(instance=perfil)
            form_caracterizacion = CaracterizacionSocioeconomicaForm(instance=perfil)
            form_password = PasswordChangeForm(request.user)

        else:  # 'personal' o cualquier otro caso
            form_personal = InformacionPersonalForm(request.POST, instance=perfil)
            if form_personal.is_valid():
                form_personal.save()
                return redirect('aprendiz:perfil')
            form_caracterizacion = CaracterizacionSocioeconomicaForm(instance=perfil)
            form_password = PasswordChangeForm(request.user)
            form_privacidad = PrivacidadForm(instance=perfil)
    else:
        form_personal = InformacionPersonalForm(instance=perfil)
        form_caracterizacion = CaracterizacionSocioeconomicaForm(instance=perfil)
        form_password = PasswordChangeForm(request.user)
        form_privacidad = PrivacidadForm(instance=perfil)

    return render(request, 'aprendiz/perfil.html', {
        'form_personal': form_personal,
        'form_caracterizacion': form_caracterizacion,
        'form_password': form_password,
        'form_privacidad': form_privacidad,
        'form_estudio': EstudioAcademicoForm(),
        'form_experiencia': ExperienciaLaboralForm(),
        'form_idioma': IdiomaForm(),
        'perfil': perfil,
    })

@aprendiz_required
def agregar_estudio(request):
    if request.method == 'POST':
        form = EstudioAcademicoForm(request.POST)
        if form.is_valid():
            estudio = form.save(commit=False)
            estudio.perfil = request.user.perfil_aprendiz
            estudio.save()
    return redirect('aprendiz:perfil')

@aprendiz_required
def eliminar_estudio(request, pk):
    estudio = get_object_or_404(EstudioAcademico, pk=pk, perfil=request.user.perfil_aprendiz)
    estudio.delete()
    return redirect('aprendiz:perfil')

@aprendiz_required
def agregar_experiencia(request):
    if request.method == 'POST':
        form = ExperienciaLaboralForm(request.POST)
        if form.is_valid():
            experiencia = form.save(commit=False)
            experiencia.perfil = request.user.perfil_aprendiz
            experiencia.save()
    return redirect('aprendiz:perfil')

@aprendiz_required
def eliminar_experiencia(request, pk):
    experiencia = get_object_or_404(ExperienciaLaboral, pk=pk, perfil=request.user.perfil_aprendiz)
    experiencia.delete()
    return redirect('aprendiz:perfil')

@aprendiz_required
def agregar_idioma(request):
    if request.method == 'POST':
        form = IdiomaForm(request.POST)
        if form.is_valid():
            idioma = form.save(commit=False)
            idioma.perfil = request.user.perfil_aprendiz
            idioma.save()
    return redirect('aprendiz:perfil')

@aprendiz_required
def eliminar_idioma(request, pk):
    idioma = get_object_or_404(Idioma, pk=pk, perfil=request.user.perfil_aprendiz)
    idioma.delete()
    return redirect('aprendiz:perfil')

@aprendiz_required
def seguimiento(request):
    perfil = request.user.perfil_aprendiz
    documentos = perfil.documentos.all()
    return render(request, 'aprendiz/seguimiento.html', {'documentos': documentos, 'perfil': perfil})

@aprendiz_required
def subir_documento(request, pk):
    documento = get_object_or_404(Documento, pk=pk, perfil=request.user.perfil_aprendiz)
    if request.method == 'POST':
        form = SubirDocumentoForm(request.POST, request.FILES, instance=documento)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.estado = 'en_revision'
            doc.save()@aprendiz_required
def subir_documento(request, pk):
    documento = get_object_or_404(Documento, pk=pk, perfil=request.user.perfil_aprendiz)
    if request.method == 'POST':
        form = SubirDocumentoForm(request.POST, request.FILES, instance=documento)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.estado = 'en_revision'
            doc.save()
            Usuario = get_user_model()
            for instructor in Usuario.objects.filter(is_instructor=True):
                notificar(
                    instructor,
                    f'{request.user.get_full_name()} subió un documento: {doc.get_tipo_documento_display()}.',
                    f'/instructor/aprendiz/{documento.perfil.pk}/',
                )
        else:
            from django.contrib import messages
            for error in form.errors.get('archivo', []):
                messages.error(request, error)
    return redirect('aprendiz:seguimiento')

@never_cache
@aprendiz_required
def seguimiento(request):
    perfil = request.user.perfil_aprendiz
    documentos = perfil.documentos.all()
    etapas = perfil.etapas.all()
    return render(request, 'aprendiz/seguimiento.html', {
        'documentos': documentos,
        'etapas': etapas,
        'perfil': perfil,
    })

