from django import forms

class OrganizacionInvitadaForm(forms.Form):
    representante_asiste = forms.BooleanField(
        required=False,
        label="¿El representante legal asistirá al evento?",
        widget=forms.CheckboxInput(attrs={
            'class': 'input-checkbox',
            'data-related': 'id_representante_alterno'
        })
    )

    representante_alterno = forms.CharField(required=False, label="Representante alterno:", max_length=100)
    
    certificado_participacion = forms.FileField(
        label="Certificado de Participación:",
        widget=forms.ClearableFileInput(attrs={
            'accept': '.pdf',
            'class': 'input-file'
        })
    )