from django import forms
from .models import *

class RegistroForm(forms.Form):
    documento = forms.CharField(label="Documento de Identidad", required=True, max_length=10)
    email = forms.EmailField(label="Correo electrónico", required=True)
    nombre = forms.CharField(label="Nombre", required=True, max_length=100)
    apellido = forms.CharField(label="Apellido", required=True, max_length=100)
    telefono = forms.CharField(label="Teléfono", required=True, max_length=10)
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar Contraseña", widget=forms.PasswordInput)

    # Selección de rol
    ROLE_CHOICES = [
        ('estudiante', 'Estudiante'),
        ('docente', 'Docente'),
        ('secretaria', 'Secretaria'),
    ]
    rol = forms.ChoiceField(label="Rol", choices=ROLE_CHOICES, required=True)

    # Campos específicos por rol (opcionales, se validan en clean())

    #* Estudiante
    codigo_estudiante = forms.CharField(required=False, label="Código de estudiante", max_length=7)
    programa = forms.ModelChoiceField(
        queryset=Programa.objects.all(),
        label="Selecciona un Programa",
        empty_label="-- Elige un Programa --",
        required=True
    )

    #* Docente
    unidadAcademica = forms.ModelChoiceField(
        queryset=UnidadAcademica.objects.all(),
        label="Selecciona una Unidad Académica",
        empty_label="-- Elige una Unidad Académica --",
        required=True
    )

    #* Secretaria
    facultad = forms.ModelChoiceField(
        queryset=Facultad.objects.all(),
        label="Selecciona una Facultad",
        empty_label="-- Elige una Facultad --",
        required=True
    )

    # Validación de campos obligatorios según rol
    def clean(self):
        cleaned_data = super().clean()
        rol = cleaned_data.get("rol")

        if rol == "estudiante":
            if not cleaned_data.get("codigo_estudiante"):
                self.add_error("codigo_estudiante", "Este campo es obligatorio para estudiantes")
            if not cleaned_data.get("programa"):
                self.add_error("programa", "Este campo es obligatorio para estudiantes")
        elif rol == "docente":
            if not cleaned_data.get("unidadAcademica"):
                self.add_error("departamento", "Este campo es obligatorio para docentes")
        elif rol == "secretaria":
            if not cleaned_data.get("facultad"):
                self.add_error("facultad", "Este campo es obligatorio para secretarias académicas")
