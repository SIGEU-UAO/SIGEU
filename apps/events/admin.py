from django.contrib import admin
from .models import *

admin.site.register(Evento)
admin.site.register(InstalacionesAsignadas)
admin.site.register(OrganizadoresEventos)
admin.site.register(OrganizacionesInvitadas)