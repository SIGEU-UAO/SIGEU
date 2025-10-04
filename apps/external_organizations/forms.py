from django import forms
from django.core.validators import RegexValidator
from .models import *

# * Validators
nit_validator = RegexValidator(regex=r'^[0-9]{8,10}-[0-9]$', message="El NIT debe contener entre 8 y 10 dígitos seguidos de un guion y un dígito de verificación")
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
    sector_economico = forms.CharField(label="Sector economico", required=True, max_length=100)
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