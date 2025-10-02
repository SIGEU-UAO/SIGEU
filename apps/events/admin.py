from django.contrib import admin
from .models import Evento, InstalacionesAsignadas, OrganizadoresEventos

admin.site.register(Evento)
admin.site.register(InstalacionesAsignadas)
admin.site.register(OrganizadoresEventos)