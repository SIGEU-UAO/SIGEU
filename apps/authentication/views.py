from django.shortcuts import render
from .forms import *

def formulario_registro(request):
    form = RegistroForm()
    return render(request, "authentication/registro.html", { "form": form })