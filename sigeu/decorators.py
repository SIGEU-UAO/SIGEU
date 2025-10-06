from django.contrib.auth.decorators import user_passes_test

def no_superuser_required(view_func=None, redirect_field_name="next", login_url="admin:index"):
    """
    Bloquea acceso a superusuarios.
    Si un superuser intenta entrar, lo redirige al admin.
    """
    actual_decorator = user_passes_test(
        lambda u: not u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator

def estudiante_required(view_func=None, redirect_field_name="next", login_url="dashboard"):
    """
    Permite acceso solo a usuarios con rol 'Estudiante'.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.rol == "Estudiante",
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator

def docente_required(view_func=None, redirect_field_name="next", login_url="dashboard"):
    """
    Permite acceso solo a usuarios con rol 'Docente'.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.rol == "Docente",
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator

def organizador_required(view_func=None, redirect_field_name="next", login_url="dashboard"):
    """
    Permite acceso a usuarios con rol 'Estudiante' o 'Docente'.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.rol in ["Estudiante", "Docente"],
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator

def secretaria_required(view_func=None, redirect_field_name="next", login_url="dashboard"):
    """
    Permite acceso solo a usuarios con rol 'Secretaria'.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.rol == "Secretaria",
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator