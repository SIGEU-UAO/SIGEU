from django import forms
from .models import *

class RegistroEventoForm(forms.Form):
    nombre = forms.CharField(label="Nombre", required=True, max_length=100)
    descripcion = forms.CharField(label="Descripcion", required=True, max_length=200)
    tipo = forms.ChoiceField(label="Tipo", choices=Evento.TIPOS, required=True)
    fecha = forms.DateField(label="Fecha", required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    horaInicio = forms.TimeField(label="Hora inicio", required=True, widget=forms.TimeInput(attrs={'type': 'time'}))
    horaFin = forms.TimeField(label="Hora fin", required=True, widget=forms.TimeInput(attrs={'type': 'time'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Force autocomplete=off on all fields
        for field in self.fields.values():
            field.widget.attrs["autocomplete"] = "off"