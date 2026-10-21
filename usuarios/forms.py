from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario


class RegistroUsuarioForm(UserCreationForm):
    ROL_CHOICES = [('aprendiz', 'Aprendiz'), ('instructor', 'Instructor')]

    rol = forms.ChoiceField(
        label='Quiero registrarme como',
        choices=ROL_CHOICES,
        initial='aprendiz',
        widget=forms.RadioSelect,
        help_text='Las cuentas de instructor deben ser aprobadas por un administrador antes de poder usarse.',
    )
    aceptar_terminos = forms.BooleanField(
        label='Acepto los términos y condiciones y la política de tratamiento de datos.',
        required=True,
    )

    field_order = [
        'rol', 'tipo_documento', 'numero_documento',
        'first_name', 'last_name', 'email',
        'password1', 'password2', 'aceptar_terminos',
    ]

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
            if isinstance(field.widget, (forms.RadioSelect, forms.CheckboxInput)):
                continue
            field.widget.attrs['class'] = 'auth-select' if name == 'tipo_documento' else 'auth-input'

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.username = usuario.numero_documento
        if self.cleaned_data['rol'] == 'instructor':
            usuario.is_aprendiz = False
            usuario.solicitud_instructor = True  # pendiente de aprobación
        else:
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
