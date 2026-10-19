import os
from django import forms
from django.core.files.uploadedfile import UploadedFile
from .models import MensajeContacto, Publicacion

class ContactoForm(forms.ModelForm):
    class Meta:
        model = MensajeContacto
        fields = ['nombre', 'email', 'asunto', 'mensaje']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej. Juan Pérez'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'tucorreo@ejemplo.com'}),
            'asunto': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Asunto de tu mensaje'}),
            'mensaje': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4, 'placeholder': '¿En qué podemos ayudarte?'}),
        }

class PublicacionForm(forms.ModelForm):
    EXTENSIONES_IMAGEN = ['.jpg', '.jpeg', '.png', '.webp']

    class Meta:
        model = Publicacion
        fields = ['titulo', 'categoria', 'resumen', 'contenido', 'imagen', 'autor', 'destacado']
        widgets = {
            'resumen': forms.Textarea(attrs={'rows': 2}),
            'contenido': forms.Textarea(attrs={'rows': 14}),
            'imagen': forms.ClearableFileInput(attrs={'accept': 'image/jpeg,image/png,image/webp'}),
        }
        help_texts = {
            'resumen': 'Máximo 300 caracteres. Se muestra en las tarjetas del blog.',
            'contenido': 'Texto plano. Separa los párrafos con una línea en blanco.',
            'imagen': 'JPG, PNG o WEBP, máximo 5 MB.',
            'destacado': 'Aparece en grande al inicio del blog.',
        }

    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen')
        if isinstance(imagen, UploadedFile):  # solo valida cuando se sube un archivo nuevo
            if os.path.splitext(imagen.name)[1].lower() not in self.EXTENSIONES_IMAGEN:
                raise forms.ValidationError('Formato no permitido. Usa JPG, PNG o WEBP.')
            if imagen.size > 5 * 1024 * 1024:
                raise forms.ValidationError('La imagen no puede superar los 5 MB.')
        return imagen
