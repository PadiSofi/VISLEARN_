from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario

class RegistroAprendizForm(UserCreationForm):
    aceptar_terminos = forms.BooleanField(
        label='Acepto los términos y condiciones y la política de tratamiento de datos.',
        required=True,
    )

    class Meta:
        model = Usuario
        fields = [
            'tipo_documento', 'numero_documento',
            'first_name', 'last_name',
            'email',
            'password1', 'password2',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        for name, field in self.fields.items():
            css_class = 'auth-select' if name == 'tipo_documento' else 'auth-input'
            field.widget.attrs['class'] = css_class

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.username = usuario.numero_documento
        usuario.is_aprendiz = True
        if commit:
            usuario.save()
        return usuario

class LoginNumeroDocumentoForm(AuthenticationForm):
    username = forms.CharField(
        label='Número de documento',
        widget=forms.TextInput(attrs={
            'placeholder': 'Ingresa tu número',
            'autofocus': True,
            'class': 'auth-input',
        }),
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••',
            'class': 'auth-input',
        }),
    )