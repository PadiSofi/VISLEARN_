from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import PerfilAprendiz, EstudioAcademico, ExperienciaLaboral, Idioma, Documento
import os

class InformacionPersonalForm(forms.ModelForm):
    class Meta:
        model = PerfilAprendiz
        fields = [
            'lugar_expedicion_documento', 'sexo_genero',
            'correo_personal', 'celular', 'telefono_fijo',
            'fecha_nacimiento', 'lugar_nacimiento',
            'direccion_residencia', 'barrio', 'municipio_departamento',
            'centro_formacion', 'programa_formacion', 'nivel_formacion',
        ]
        widgets = {'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'})}

class CaracterizacionSocioeconomicaForm(forms.ModelForm):
    class Meta:
        model = PerfilAprendiz
        fields = [
            'ocupacion_perfil_productivo', 'zona_residencial',
            'estrato_socioeconomico', 'grupo_sisben', 'medio_transporte',
            'estado_civil', 'numero_hijos', 'eps', 'arl',
            'tipo_sangre', 'libreta_militar',
            'discapacidad_condicion_especial', 'multiculturalidad_enfoque_diferencial',
        ]

class EstudioAcademicoForm(forms.ModelForm):
    class Meta:
        model = EstudioAcademico
        fields = ['titulo', 'institucion', 'fecha_inicio', 'fecha_fin', 'en_curso']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
        }

class ExperienciaLaboralForm(forms.ModelForm):
    class Meta:
        model = ExperienciaLaboral
        fields = ['cargo', 'empresa', 'fecha_inicio', 'fecha_fin', 'actual', 'descripcion']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
        }

class IdiomaForm(forms.ModelForm):
    class Meta:
        model = Idioma
        fields = ['idioma', 'nivel']

class PrivacidadForm(forms.ModelForm):
    class Meta:
        model = PerfilAprendiz
        fields = ['recibir_notificaciones_email', 'autorizar_tratamiento_datos']

class SubirDocumentoForm(forms.ModelForm):
    EXTENSIONES_PERMITIDAS = ['.pdf', '.jpg', '.jpeg', '.png']
    class Meta:
        model = Documento
        fields = ['archivo']
    def clean_archivo(self):
        archivo = self.cleaned_data.get('archivo')
        if archivo:
            extension = os.path.splitext(archivo.name)[1].lower()
            if extension not in self.EXTENSIONES_PERMITIDAS:
                raise forms.ValidationError(
                    f'Formato no permitido ({extension}). Solo se aceptan: PDF, JPG, JPEG, PNG.'
                )
            if archivo.size > 10 * 1024 * 1024:
                raise forms.ValidationError('El archivo no puede superar los 10 MB.')
        return archivo
