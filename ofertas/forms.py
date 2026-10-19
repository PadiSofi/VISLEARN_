from django import forms
from .models import OfertaLaboral, Postulacion

class OfertaLaboralForm(forms.ModelForm):
    class Meta:
        model = OfertaLaboral
        fields = [
            'titulo', 'empresa', 'pais', 'ciudad', 'modalidad', 'salario',
            'tipo_visa', 'idioma_requerido', 'tecnologias',
            'descripcion', 'requisitos', 'beneficios',
            'enlace_externo', 'fecha_cierre', 'activa',
        ]
        widgets = {
            'fecha_cierre': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'descripcion': forms.Textarea(attrs={'rows': 5}),
            'requisitos': forms.Textarea(attrs={'rows': 5}),
            'beneficios': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_enlace_externo(self):
        enlace = self.cleaned_data.get('enlace_externo', '')
        if enlace and not enlace.lower().startswith(('http://', 'https://')):
            raise forms.ValidationError('El enlace debe empezar por http:// o https://')
        return enlace

class ActualizarPostulacionForm(forms.ModelForm):
    class Meta:
        model = Postulacion
        fields = ['estado', 'notas']
        widgets = {
            'notas': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Notas: fecha de entrevista, contacto, respuesta...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['estado'].choices = [c for c in Postulacion.ESTADO_CHOICES if c[0] != 'guardada']
        self.fields['estado'].widget.attrs['aria-label'] = 'Estado de la postulación'
        self.fields['notas'].widget.attrs['aria-label'] = 'Notas'
