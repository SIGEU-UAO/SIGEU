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
