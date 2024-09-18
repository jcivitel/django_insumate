from functools import wraps

from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect


def check_registration_enabled(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not settings.REGISTRATION_ENABLED:
            messages.error(request, "registration is not enabled")
            return redirect("login")
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def not_logged_in(user):
    return not user.is_authenticated
