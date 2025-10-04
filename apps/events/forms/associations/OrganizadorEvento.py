from django import forms

class OrganizadorEventoForm(forms.Form):
    aval = forms.FileField(
        label="Aval del Organizador:",
        widget=forms.ClearableFileInput(attrs={
            'accept': '.pdf',
            'class': 'input-file'
        })
    )