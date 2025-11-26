from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from apps.events.services.event import EventoService
from .forms import RegistroForm, InicioSesionForm, EditarPerfilForm, CustomPasswordResetForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView
from django.contrib.auth import get_user_model
from django.contrib import messages
from sigeu.decorators import no_superuser_required
from .service import save_password_history, validate_new_password
import json
from django.contrib.auth.views import PasswordResetConfirmView

def formulario_registro(request):
    form = RegistroForm()
    return render(request, "users/registro.html", {"form": form, "password_icons": ["ri-eye-fill", "ri-information-2-fill" ]})


def inicio_sesion(request):
    # If already authenticated, redirect to the dashboard
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("dashboard"))

    form = InicioSesionForm()
    return render(request, "users/inicio_sesion.html", {"form": form, "password_icons": ["ri-eye-fill"]})

@no_superuser_required
@login_required
def dashboard(request):
    notificaciones = EventoService.obtener_notificaciones(request.user)

    return render(request, "users/dashboard.html", {
        "header_title": f"Hola, {request.user.nombres} {request.user.apellidos} 👋", 
        "header_paragraph": "Bienvenido de vuelta a SIGEU",
        "active_page": "dashboard",
        "notificaciones": notificaciones,
    })

@no_superuser_required
@login_required
def editar_perfil(request):
    initial_data = {
        "numeroIdentificacion": request.user.numero_identificacion,
        "nombres": request.user.nombres,
        "apellidos": request.user.apellidos,
        "email": request.user.email,
        "telefono": request.user.telefono,
        "contraseña": ""
    }

    notificaciones = EventoService.obtener_notificaciones(request.user)
    form = EditarPerfilForm(initial=initial_data, user=request.user)
    return render(request, "users/editar_perfil.html", {"form": form, "active_page": "perfil", "notificaciones": notificaciones})

# ----- Password Reset Views -----

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'users/reset_password/password_reset_form.html'
    email_template_name = 'users/reset_password/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')
    
    def dispatch(self, request, *args, **kwargs):
        if request.headers.get("Content-Type") == "application/json":
            try:
                data = json.loads(request.body)
                request.POST = request.POST.copy()
                for key, value in data.items():
                    request.POST[key] = value
            except json.JSONDecodeError:
                return JsonResponse({"success": False, "message": "JSON inválido"}, status=400)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        email = form.cleaned_data['email']

        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            if self.request.headers.get("Content-Type") == "application/json":
                return JsonResponse({"success": False, "message": "Correo no registrado"}, status=404)
            messages.error(self.request, 'Correo no registrado')
            return self.render_to_response(self.get_context_data(form=form))

        try:
            self.request.session['password_reset_email'] = email
            response = super().form_valid(form)
            if self.request.headers.get("Content-Type") == "application/json":
                return JsonResponse({
                    "success": True,
                    "message": f"Se ha enviado un correo de recuperación a {email}"
                }, status=200)

            return response 

        except Exception as e:
            if self.request.headers.get("Content-Type") == "application/json":
                return JsonResponse({"success": False, "message": f"Error al enviar correo: {str(e)}"}, status=500)
            messages.error(self.request, f'Error al enviar correo: {str(e)}')
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        if self.request.headers.get("Content-Type") == "application/json":
            return JsonResponse({
                "success": False,
                "errors": form.errors.get_json_data()
            }, status=400)

        # Converts errors in the form to messages to show with JS
        if 'email' in form.errors:
            for error in form.errors['email']:
                messages.error(self.request, str(error))
        
        # Cleans errors in the form to avoid duplicates
        form.errors.clear()
        
        return self.render_to_response(self.get_context_data(form=form))
    
    
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/reset_password/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

    def _is_json_request(self, request):
        ct = request.META.get('CONTENT_TYPE', '') or request.headers.get('Content-Type', '')
        accept = request.META.get('HTTP_ACCEPT', '') or request.headers.get('Accept', '')
        return 'application/json' in ct.lower() or 'application/json' in accept.lower()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['validlink'] = self.validlink
        return context


    def get(self, request, *args, **kwargs):
        if not self.validlink:
            if self._is_json_request(request):
                return JsonResponse({
                    "success": False,
                    "message": "El enlace de restablecimiento no es válido o ha expirado."
                }, status=400)
        return super().get(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if self._is_json_request(request):
            try:
                data = json.loads(request.body or b'{}')
                request.POST = request.POST.copy()
                for key, value in data.items():
                    request.POST[key] = value
            except json.JSONDecodeError:
                return JsonResponse({"success": False, "message": "JSON inválido"}, status=400)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Guarda la nueva contraseña
        try:
            validate_new_password(
                form.user,
                form.cleaned_data['new_password1']
            )
            save_password_history(form.user)
        except ValueError as e:
            if self._is_json_request(self.request):
                return JsonResponse({"success": False, "message": str(e)}, status=400)
            messages.error(self.request, str(e))
            return self.form_invalid(form)


        form.save()
        if self._is_json_request(self.request):
            return JsonResponse({"success": True, "message": "Contraseña restablecida correctamente."}, status=200)
        return super().form_valid(form)

    def form_invalid(self, form):
        if self._is_json_request(self.request):
            return JsonResponse({"success": False, "errors": form.errors.get_json_data()}, status=400)
        return super().form_invalid(form)

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/reset_password/password_reset_done.html'

    def get(self, request, *args, **kwargs):
        try:
            email = request.session.pop('password_reset_email', None)
            if request.headers.get("Content-Type") == "application/json":
                if email:
                    return JsonResponse({
                        "success": True,
                        "message": f"Se ha enviado un correo de recuperación a {email}"
                    }, status=200)
                else:
                    return JsonResponse({
                        "success": True,
                        "message": "Se ha enviado un correo de recuperación a tu dirección de email."
                    }, status=200)

            if email:
                messages.success(request, f'Se ha enviado un correo de recuperación a {email}')
            else:
                messages.success(request, 'Se ha enviado un correo de recuperación a tu dirección de email.')
            return super().get(request, *args, **kwargs)
        except Exception as e:
            if request.headers.get("Content-Type") == "application/json":
                return JsonResponse({
                    "success": False,
                    "message": f"Error interno del servidor: {str(e)}"
                }, status=500)

            messages.error(request, f"Error interno del servidor: {str(e)}")
            return super().get(request, *args, **kwargs)

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/reset_password/password_reset_complete.html'