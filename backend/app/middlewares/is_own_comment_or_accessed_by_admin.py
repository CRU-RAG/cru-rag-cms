"""Middleware to check if users are accessing their own comments or admin access"""

from functools import wraps
from flask import abort

from app.models.user import User
from app.utils.comment_helpers import get_comment_and_user


def is_own_comment_or_accessed_by_admin(f):
    """Decorator to check if users are accessing their own comments or admin access"""

    @wraps(f)
    def wrapper(*args, **kwargs):
        current_user_id, comment = get_comment_and_user(**kwargs)
        current_user = User.query.get(current_user_id)
        if comment.user_id == current_user_id or current_user.role == "admin":
            return f(*args, **kwargs)
        abort(403, description="Access restricted to the user or admin.")

    return wrapper
