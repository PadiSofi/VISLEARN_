from functools import wraps
from django.core.exceptions import PermissionDenied

def instructor_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_instructor:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper

def aprendiz_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_aprendiz:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper

def administrador_required(view_func):
    """Solo el administrador (superusuario)."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper

def contenido_required(view_func):
    """Instructores y administrador: gestión de blog y ofertas."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated or not (user.is_instructor or user.is_superuser):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper
