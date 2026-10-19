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

