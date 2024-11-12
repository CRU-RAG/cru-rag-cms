"""Middleware to check regular user access"""

from functools import wraps
from flask import abort

from app.middlewares.authorization import verify_active_user


def is_regular(f):
    """Decorator to check regular user access"""

    @verify_active_user
    @wraps(f)
    def wrapper(current_user, *args, **kwargs):
        if current_user.role != "regular":
            abort(403, description="Regular user access required.")
        return f(*args, **kwargs)

    return wrapper
