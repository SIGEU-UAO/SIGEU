from django import forms
from django.core.validators import RegexValidator
from .models import *
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from email.mime.image import MIMEImage
from email.utils import make_msgid
from pathlib import Path
import re
from html import unescape

# Utilidad simple para convertir HTML -> texto con saltos de línea legibles
# sin depender de una plantilla .txt aparte.
def _html_to_text(html):
    text = html
    # Reemplazos básicos para conservar estructura
    patterns = [
        (r'<br\s*/?>', '\n'),
        (r'</p>', '\n\n'),
        (r'<h[1-6][^>]*>', '\n'),
        (r'</h[1-6]>', '\n\n'),
        (r'<li[^>]*>', '• '),
        (r'</li>', '\n'),
        (r'<ul[^>]*>', '\n'),
        (r'</ul>', '\n'),
        (r'<ol[^>]*>', '\n'),
        (r'</ol>', '\n'),
        (r'<div[^>]*>', '\n'),
        (r'</div>', '\n'),
        (r'<[^>]+>', ''),  # Remover todas las demás etiquetas HTML
    ]
    
    for pattern, replacement in patterns:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    # Limpiar espacios en blanco excesivos
    text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    
    return unescape(text.strip())

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
        widget=forms.PasswordInput(attrs={ "class": "password-field" }),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Force autocomplete=off on all fields
        for field in self.fields.values():
            field.widget.attrs["autocomplete"] = "off"

class EditarPerfilForm(forms.Form):
    numeroIdentificacion = forms.CharField(
        label="Documento de Identidad",
        required=True,
        min_length=8,
        max_length=10,
        validators=[numero_identificacion_validator],
        widget=forms.TextInput(attrs={
            "readonly": "true",
            "class": "numeric-field",
            "pattern": r"[0-9]{8,10}",
            "title": "El documento debe contener entre 8 y 10 números"
        })
    )
    nombres = forms.CharField(
        label="Nombres",
        required=True,
        widget=forms.TextInput(attrs={"disabled": "true"})
    )
    apellidos = forms.CharField(
        label="Apellidos",
        required=True,
        widget=forms.TextInput(attrs={"disabled": "true"})
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
            "disabled": "true"
        })
    )
    contraseña = forms.CharField(
        label="Contraseña",
        required=False,
        widget=forms.PasswordInput(attrs={
            "class": "password-field",
            "pattern": r"^(?:|(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,})$",
            "title": "La contraseña debe tener mínimo 8 caracteres, al menos una mayúscula, una minúscula y un número",
            "placeholder": "Dejar vacío si no desea cambiar"
        }),
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        # Force autocomplete=off on all fields
        for field in self.fields.values():
            field.widget.attrs["autocomplete"] = "off"

    def clean_contraseña(self):
        value = self.cleaned_data.get("contraseña", "")
        if value is None:
            value = ""
        value = value.strip()
        # If empty, do not enforce complexity
        if value == "":
            return ""
        # Enforce complexity only when provided
        password_validator(value)
        return value
    
class ModalBuscarOrganizadorForm(forms.Form):
    nombre_completo = forms.CharField(label="Nombre Completo", required=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Force autocomplete=off on all fields
        for field in self.fields.values():
            field.widget.attrs["autocomplete"] = "off"

class CustomPasswordResetForm(PasswordResetForm):
    """
    Formulario de reset de contraseña que define el asunto en código,
    evitando el uso de subject_template_name.
    """
    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        subject = "SIGEU - Recuperación de Contraseña"

        # Preparar contexto (posible copia) y CID del banner
        ctx = dict(context or {})
        banner_cid = make_msgid(domain=None)[1:-1]  # quitar <>
        ctx['banner_cid'] = banner_cid

        # Renderizar el HTML del correo (incluye cid en la plantilla)
        html_template = html_email_template_name or email_template_name
        html_body = render_to_string(html_template, ctx)

        # Cuerpo de texto plano derivado del HTML (sin plantilla .txt)
        text_body = _html_to_text(html_body)

        email_message = EmailMultiAlternatives(subject, text_body, from_email, [to_email])
        email_message.attach_alternative(html_body, "text/html")

        # Adjuntar banner como imagen inline usando el path del proyecto
        try:
            banner_path = Path(settings.BASE_DIR) / 'static' / 'assets' / 'img' / 'banner.png'
            with open(banner_path, 'rb') as f:
                img = MIMEImage(f.read())
                img.add_header('Content-ID', f'<{banner_cid}>')
                img.add_header('Content-Disposition', 'inline', filename='banner.png')
                email_message.attach(img)
        except Exception:
            # Si falla, el HTML seguirá usando el fallback por URL absoluta
            pass

        email_message.send()
