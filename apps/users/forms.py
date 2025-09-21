from django import forms
from django.core.validators import RegexValidator
from .models import *

# * Validators
numero_identificacion_validator = RegexValidator(regex=r'^[0-9]{8,10}$', message="El documento debe contener entre 8 y 10 números.")
email_validator = RegexValidator(regex=r'^[A-Za-z0-9._%+-]+@uao\.edu\.co$', message="Ingresa un correo electrónico válido.")
telefono_validator = RegexValidator(regex=r'^[0-9]{1,10}$', message="El teléfono solo puede contener hasta 10 números.")
password_validator = RegexValidator(regex=r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$', message="La contraseña debe tener mínimo 8 caracteres, al menos una mayúscula, una minúscula y un número.")
codigo_validator = RegexValidator(regex=r'^[0-9]{7}$', message="El código de estudiante debe tener exactamente 7 dígitos.")

class RegistroForm(forms.Form):
    documento = forms.CharField(
        label="Documento de Identidad",
        required=True,
        max_length=10,
        min_length=8,
        validators=[numero_identificacion_validator],
        widget=forms.TextInput(attrs={
            "class": "numeric-field",
            "pattern": r"[0-9]{8,10}",
            "title": "El documento debe contener entre 8 y 10 números"
        })
    )
    email = forms.EmailField(
        label="Correo electrónico",
        required=True,
        validators=[email_validator],
        widget=forms.EmailInput(attrs={
            "pattern": "^[A-Za-z0-9._%+\-]+@uao\.edu\.co$",
            "title": "Ingresa un correo electrónico válido"
        })
    )
    nombre = forms.CharField(label="Nombre", required=True, max_length=100)
    apellido = forms.CharField(label="Apellido", required=True, max_length=100)
    telefono = forms.CharField(
        label="Teléfono",
        required=True,
        min_length=10,
        max_length=10,
        validators=[telefono_validator],
        widget=forms.TextInput(attrs={
            "type": "tel",
            "class": "numeric-field",
            "pattern": r"[0-9]{1,10}",
            "title": "El teléfono debe contener 10 números"
        })
    )
    password1 = forms.CharField(
        label="Contraseña",
        validators=[password_validator],
        widget=forms.PasswordInput(attrs={
            "class": "password-field",
            "pattern": r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$",
            "title": "La contraseña debe tener mínimo 8 caracteres, al menos una mayúscula, una minúscula y un número"
        }),
    )
    password2 = forms.CharField(
        label="Confirmar Contraseña",
        validators=[password_validator],
        widget=forms.PasswordInput(attrs={
            "class": "password-field",
            "pattern": r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$",
            "title": "La contraseña debe tener mínimo 8 caracteres, al menos una mayúscula, una minúscula y un número"
        }),
    )

    # Selección de rol
    ROLE_CHOICES = [
        ('estudiante', 'Estudiante'),
        ('docente', 'Docente'),
        ('secretaria', 'Secretaria'),
    ]
    rol = forms.ChoiceField(label="Rol", choices=ROLE_CHOICES, required=True)

    # Campos específicos por rol (opcionales, se validan en clean())

    #* Estudiante
    codigo_estudiante = forms.CharField(
        label="Código de estudiante",
        required=False,
        min_length=7,
        max_length=7,
        validators=[codigo_validator],
        widget=forms.TextInput(attrs={
            "class": "numeric-field",
            "pattern": r"[0-9]{7}",
            "title": "El código de estudiante debe tener exactamente 7 dígitos"
        })
    )
    programa = forms.ModelChoiceField(
        queryset=Programa.objects.all(),
        label="Selecciona un Programa",
        empty_label="-- Elige un Programa --",
        required=False
    )

    #* Docente
    unidadAcademica = forms.ModelChoiceField(
        queryset=UnidadAcademica.objects.all(),
        label="Selecciona una Unidad Académica",
        empty_label="-- Elige una Unidad Académica --",
        required=False,
        disabled=True # By default
    )

    #* Secretaria
    facultad = forms.ModelChoiceField(
        queryset=Facultad.objects.all(),
        label="Selecciona una Facultad",
        empty_label="-- Elige una Facultad --",
        required=False,
        disabled=True # By default
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Force autocomplete=off on all fields
        for field in self.fields.values():
            field.widget.attrs["autocomplete"] = "off"

class InicioSesionForm(forms.Form):
    email = forms.EmailField(
        label="Correo electrónico",
        required=True,
        validators=[RegexValidator(
            regex=email_validator.regex,
            message="Ingresa un correo válido. Ejemplo: usuario@dominio.com"
        )]
    )
    password = forms.CharField(
        label="Contraseña",
        required=True,
        validators=[RegexValidator(
            regex=password_validator.regex,
            message=("La contraseña debe tener al menos 8 caracteres, "
                     "incluyendo una mayúscula, una minúscula y un número.")
        )],
        widget=forms.PasswordInput(attrs={
            "class": "password-field",
            "pattern": r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$",
            "title": "La contraseña debe tener mínimo 8 caracteres, al menos una mayúscula, una minúscula y un número"
        }),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Force autocomplete=off on all fields
        for field in self.fields.values():
            field.widget.attrs["autocomplete"] = "off"
class EditarPerfil(forms.Form):  
    numeroIdentificacion = forms.CharField(
        label="Documento de Identidad",
        required=True,
        widget=forms.TextInput(attrs={"readonly": "true"})
    )
    nombres = forms.CharField(
        label="Nombres",
        required=True,
        widget=forms.TextInput(attrs={"disabled": "true"})
    )
    apellidos = forms.CharField(
        label="Apellidos",
        required=True,
        widget=forms.TextInput(attrs={"readonly": "true"})
    )
    email = forms.EmailField(
        label="Email",
        required=True,
        widget=forms.EmailInput(attrs={"disabled": "true"})
    )
    telefono = forms.CharField(
        label="Teléfono",
        required=True,
        min_length=10,
        max_length=10,
        validators=[telefono_validator],
        widget=forms.TextInput(attrs={
            "type": "tel",
            "class": "numeric-field",
            "pattern": r"[0-9]{1,10}",
            "title": "El teléfono debe contener 10 números",
            "readonly": "true"
        })
    )
    #* Estudiante
    codigo_estudiante = forms.CharField(
        label="Código de estudiante",
        required=False,
        min_length=7,
        max_length=7,
        validators=[codigo_validator],
        widget=forms.TextInput(attrs={
            "class": "numeric-field",
            "pattern": r"[0-9]{7}",
            "title": "El código de estudiante debe tener exactamente 7 dígitos"
        })
    )

    contraseña = forms.CharField(
        label="Contraseña",
        required=False,
        validators=[password_validator],
        widget=forms.PasswordInput(attrs={
            "class": "password-field",
            "pattern": r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$",
            "title": "La contraseña debe tener mínimo 8 caracteres, al menos una mayúscula, una minúscula y un número"
        }),
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        # Force autocomplete=off on all fields
        for field in self.fields.values():
            field.widget.attrs["autocomplete"] = "off"

        # if the user is not a strudent, remove field
        if not user or user.rol != "Estudiante":
            self.fields.pop("codigo_estudiante", None)