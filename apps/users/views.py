from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .forms import RegistroForm, InicioSesionForm, EditarPerfilForm, CustomPasswordResetForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView
from django.contrib.auth import get_user_model
from django.contrib import messages
from sigeu.decorators import no_superuser_required
from .service import UserService
import json
import logging

def formulario_registro(request):
    if request.method == "GET":
        form = RegistroForm()
        return render(request, "users/registro.html", {"form": form, "password_icons": ["ri-eye-fill", "ri-information-2-fill" ]})
    return JsonResponse({"error": "Método no permitido"}, status=405)


def inicio_sesion(request):
    # If already authenticated, redirect to the dashboard
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("dashboard"))

    if request.method == "GET":
        form = InicioSesionForm()
        return render(request, "users/inicio_sesion.html", {"form": form, "password_icons": ["ri-eye-fill"]})
    return JsonResponse({"error": "Método no permitido"}, status=405)

@no_superuser_required
@login_required()
def dashboard(request):
    if request.method == "GET":
        return render(request, "users/dashboard.html", {
            "header_title": f"Hola, {request.user.nombres} {request.user.apellidos} 👋", 
            "header_paragraph": "Bienvenido de vuelta a SIGEU",
            "active_page": "dashboard"
        })
    return JsonResponse({"error": "Método no permitido"}, status=405)

@no_superuser_required
@login_required()
def editar_perfil(request):
    if request.method == "GET":
        initial_data = {
            "numeroIdentificacion": request.user.numeroIdentificacion,
            "nombres": request.user.nombres,
            "apellidos": request.user.apellidos,
            "email": request.user.email,
            "telefono": request.user.telefono,
            "contraseña": ""
        }
        form = EditarPerfilForm(initial=initial_data, user=request.user)
        return render(request, "users/editar_perfil.html", {"form": form, "active_page": "perfil"})
    return JsonResponse({"error": "Método no permitido"}, status=405)

# ----- Password Reset Views -----
logger = logging.getLogger(__name__)

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'users/reset_password/password_reset_form.html'
    email_template_name = 'users/reset_password/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        """Valida existencia de email y guarda email en sesión"""
        email = form.cleaned_data['email']
        logger.info(f"Intentando enviar correo de reset a: {email}")
        User = get_user_model()
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            logger.warning(f"Intento de reset con email no registrado: {email}")
            messages.error(self.request, 'El correo electrónico no está registrado en SIGEU.')
            return self.render_to_response(self.get_context_data(form=form))
        try:
            self.request.session['password_reset_email'] = email
            response = super().form_valid(form)
            logger.info(f"Correo de reset enviado exitosamente a: {email}")
            return response
        except Exception as e:
            logger.error(f"Error al enviar correo de reset a {email}: {str(e)}")
            messages.error(self.request, f'Error al enviar correo: {str(e)}')
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        logger.error(f"Formulario de password reset inválido: {form.errors}")
        messages.error(self.request, 'Por favor corrige los errores en el formulario')
        return super().form_invalid(form)

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/reset_password/password_reset_done.html'

    def get(self, request, *args, **kwargs):
        email = request.session.pop('password_reset_email', None)
        if email:
            messages.success(request, f'Se ha enviado un correo de recuperación a {email}')
        else:
            messages.success(request, 'Se ha enviado un correo de recuperación a tu dirección de email.')
        return super().get(request, *args, **kwargs)

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/reset_password/password_reset_complete.html'