from django import forms

class ModalBuscarInstalacionForm(forms.Form):
    ubicacion = forms.CharField(label="Ubicación", required=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Force autocomplete=off on all fields
        for field in self.fields.values():
            field.widget.attrs["autocomplete"] = "off"