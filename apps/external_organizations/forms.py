from django import forms
from django.core.validators import RegexValidator
from .models import *

# * Validators
nit_validator = RegexValidator(regex=r'^[1-9][0-9]{7,9}-[0-9]$', message="El NIT debe contener entre 8 y 10 dígitos seguidos de un guion y un dígito de verificación")
telefono_validator = RegexValidator(regex=r'^[0-9]{10}$', message="El teléfono solo puede contener hasta 10 números.")

class RegistroForm(forms.Form):
    nit = forms.CharField(
        label="NIT",
        required=True,
        max_length=11,
        min_length=11,
        validators=[nit_validator],
        widget=forms.TextInput(attrs={
            "class": "numeric-field",
            "pattern": r'^[0-9]{9}-[0-9]$',
            "title": "El NIT debe contener entre 8 y 10 números"
        })
    )
    nombre = forms.CharField(label="Nombre", required=True, max_length=100)
    representante_legal = forms.CharField(label="Representante Legal", required=True, max_length=100)
    telefono = forms.CharField(
        label="Teléfono",
        required=True,
        min_length=10,
        max_length=10,
        validators=[telefono_validator],
        widget=forms.TextInput(attrs={
            "type": "tel",
            "class": "numeric-field",
            "pattern": r"[0-9]{10}",
            "title": "El teléfono debe contener 10 números"
        })
    )
    ubicacion = forms.CharField(label="Ubicacion", required=True, max_length=100)

    # select sector_economico
    SECTORES_ECONOMICOS_CHOICES = [
        ('Educacion y Ciencia', 'Educación y Ciencia'),
        ('Tecnologia y Comunicaciones', 'Tecnología y Comunicaciones'),
        ('Salud y Bienestar', 'Salud y Bienestar'),
        ('Empresarial e Industrial', 'Empresarial e Industrial'),
        ('Finanzas y Servicios profesionales', 'Finanzas y Servicios Profesionales'),
        ('Cultura y Medios', 'Cultura y Medios'),
        ('Medio Ambiente y Sostenibilidad', 'Medio Ambiente y Sostenibilidad'),
        ('Gobierno y Organismos publicos', 'Gobierno y Organismos Públicos'),
        ('Organizaciones sociales y ONGs', 'Organizaciones Sociales y ONGs'),
        ('Turismo, Hoteleria y Gastronomia', 'Turismo, Hotelería y Gastronomía'),
        ('Comercio y Consumo', 'Comercio y Consumo'),
        ('Otro', 'Otro'),
    ]

    sector_economico = forms.ChoiceField(
        label="Sector economico",
        required=True,
        choices=SECTORES_ECONOMICOS_CHOICES
    )

    actividad_principal = forms.CharField(label="Actividad principal", required=True, max_length=200)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Force autocomplete=off on all fields
        for field in self.fields.values():
            field.widget.attrs["autocomplete"] = "off"

class ModalBuscarOrganizacionForm(forms.Form):
    nit = forms.CharField(
        label="NIT",
        required=True,
        max_length=11,
        widget=forms.TextInput(attrs={"class": "numeric-field"})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Force autocomplete=off on all fields
        for field in self.fields.values():
            field.widget.attrs["autocomplete"] = "off"