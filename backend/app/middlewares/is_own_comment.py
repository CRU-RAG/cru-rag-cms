"""Middleware to check if users are accessing their own comments"""

from functools import wraps
from flask import abort

from app.services.comment_services import get_comment_and_user


def is_own_comment(f):
    """Decorator to check if users are accessing their own comments"""

    @wraps(f)
    def wrapper(*args, **kwargs):
        current_user_id, comment = get_comment_and_user(**kwargs)
        if comment.user_id == current_user_id:
            return f(*args, **kwargs)
        abort(403, description="Access restricted to the user.")

    return wrapper
