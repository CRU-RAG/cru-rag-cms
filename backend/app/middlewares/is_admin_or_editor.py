"""Middleware to check admin access or editor access"""

from functools import wraps
from flask import abort

from app.middlewares.authorization import verify_active_user


def is_admin_or_editor(f):
    """Decorator to check admin access or editor access"""

    @verify_active_user
    @wraps(f)
    def wrapper(current_user, *args, **kwargs):
        if current_user.role in ["admin", "editor"]:
            return f(*args, **kwargs)
        abort(
            403,
            description="Access forbidden: Only admins or editors can access this resource.",
        )

    return wrapper
