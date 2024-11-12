"""Middleware to check editor access"""

from functools import wraps
from flask import abort

from app.middlewares.authorization import verify_active_user


def is_editor(f):
    """Decorator to check editor access"""

    @verify_active_user
    @wraps(f)
    def wrapper(current_user, *args, **kwargs):
        if current_user.role != "editor":
            abort(403, description="Editor access required.")
        return f(*args, **kwargs)

    return wrapper
