from django import forms
from datetime import date
from ..models import Evento, EvaluacionEvento

class RegistroEventoForm(forms.Form):
    nombre = forms.CharField(label="Nombre", required=True, max_length=100)
    tipo = forms.ChoiceField(label="Tipo", choices=Evento.TIPOS, required=True)
    descripcion = forms.CharField(label="Descripcion", required=True, max_length=200, widget=forms.Textarea())
    capacidad = forms.IntegerField(label="Capacidad", required=True, widget=forms.NumberInput(attrs={"class": "numeric-field", "min": '1'}))
    fecha = forms.DateField(label="Fecha", required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    horaInicio = forms.TimeField(label="Hora inicio", required=True, widget=forms.TimeInput(attrs={'type': 'time'}))
    horaFin = forms.TimeField(label="Hora fin", required=True, widget=forms.TimeInput(attrs={'type': 'time'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Force autocomplete=off on all fields
        for field in self.fields.values():
            field.widget.attrs["autocomplete"] = "off"

    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get("fecha")
        hora_inicio = cleaned_data.get("horaInicio")
        hora_fin = cleaned_data.get("horaFin")
        capacidad = cleaned_data.get("capacidad")

        # Validate that the date is not earlier than today
        if fecha and fecha < date.today():
            self.add_error("fecha", "La fecha del evento debe ser igual o posterior a la fecha actual.")

        # Validate that the end time is greater than the start time.
        if hora_inicio and hora_fin and hora_fin <= hora_inicio:
            self.add_error("horaFin", "La hora de fin debe ser mayor que la hora de inicio.")

        # Validate that the capacity is greater than 0
        if capacidad and capacidad <= 0:
            self.add_error("capacidad", "La capacidad debe ser mayor a 0.")

        return cleaned_data

class EvaluacionEventoForm(forms.Form):
    tipo = forms.ChoiceField(label="Tipo", choices=EvaluacionEvento.TIPOS_EVALUACION, required=True, widget=forms.Select(attrs={"id": "tipo-evaluacion"}))
    acta = forms.FileField(label="Acta de Aprobación", widget=forms.FileInput(attrs={"accept": ".pdf", "id": "acta-aprobacion", "class": "input-file"}))
    justificacion = forms.CharField(label="Justificación", disabled=True, widget=forms.Textarea(attrs={"id": "justificacion", "minlength": '10'}))