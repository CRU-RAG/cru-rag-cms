"""Middleware to check if a user is admin"""

from functools import wraps
from flask import abort

from app.middlewares.authorization import verify_active_user


def is_admin(f):
    """Decorator for checking admin status"""

    @verify_active_user
    @wraps(f)
    def wrapper(current_user, *args, **kwargs):
        if current_user.role != "admin":
            abort(403, description="Admin access required.")
        return f(*args, **kwargs)

    return wrapper
