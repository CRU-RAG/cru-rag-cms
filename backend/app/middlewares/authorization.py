"""Middleware to verify that the JWT is valid and the user is active."""

from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask import abort
from app.models.user import User


def verify_active_user(f):
    """Decorator to verify that the JWT is valid and the user is active."""

    @wraps(f)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        if not current_user or current_user.deleted_at is not None:
            abort(401, description="Invalid or missing authentication token.")
        return f(current_user, *args, **kwargs)

    return wrapper
