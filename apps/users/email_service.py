from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def send_email(subject, to_email, template_name=None, context=None, text_body=None):
    if context is None:
        context = {}

    # Renderiza el cuerpo HTML si hay plantilla
    html_body = render_to_string(template_name, context) if template_name else None

    # Crea el correo
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_body or "",  # texto alternativo si el cliente no soporta HTML
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[to_email] if isinstance(to_email, str) else to_email,
    )

    # Adjunta versión HTML (si existe)
    if html_body:
        email.attach_alternative(html_body, "text/html")

    # Envía
    email.send(fail_silently=False)