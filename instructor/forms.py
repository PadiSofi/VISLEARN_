from django import forms
from aprendiz.models import Documento, EtapaSeguimiento

class RevisarDocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['estado', 'observaciones_instructor']
        widgets = {
            'observaciones_instructor': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Observación para el aprendiz (opcional)'}),
        }

class ActualizarEtapaForm(forms.ModelForm):
    class Meta:
        model = EtapaSeguimiento
        fields = ['estado', 'observaciones']
        widgets = {
            'observaciones': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Observación (opcional)'}),
        }