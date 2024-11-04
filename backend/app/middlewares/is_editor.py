"""Middleware to check editor access"""
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask import abort
from ..models.user import User

def is_editor(f):
    """Decorator to check editor access"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        if not current_user or current_user.deleted_at is not None:
            abort(401, description="Invalid or missing authentication token.")
        if current_user.role != 'editor':
            abort(403, description="Editor access required.")
        return f(*args, **kwargs)
    return wrapper
