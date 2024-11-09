"""Middleware to check admin access or user's own data access"""

from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask import abort
from ..models.user import User


def is_admin_or_self(f):
    """Decorator to check admin access or user's own data access"""

    @wraps(f)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        current_user_id = get_jwt_identity()
        request_user_id = kwargs.get("user_id")
        current_user = User.query.get(current_user_id)
        if not current_user or current_user.deleted_at is not None:
            abort(401, description="Invalid or missing authentication token.")
        if current_user.role == "admin" or current_user_id == request_user_id:
            return f(*args, **kwargs)
        abort(
            403,
            description="Access forbidden: \
                Only admin or the concerned user can access this resource.",
        )

    return wrapper
