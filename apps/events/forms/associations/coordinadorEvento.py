from django import forms
from ...validations.data_validators import validate_pdf

class CoordinadorEventoForm(forms.Form):
    aval = forms.FileField(
        label="Aval del Organizador:",
        validators=[validate_pdf],
        widget=forms.ClearableFileInput(attrs={
            'accept': '.pdf',
            'class': 'input-file'
        })
    )