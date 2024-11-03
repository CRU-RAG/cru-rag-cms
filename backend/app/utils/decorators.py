"""Custom decorators for role-based access control."""
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask import abort
from ..models.user import User
from ..extensions import DB as db

def roles_required(*required_roles):
    """Decorator to check if a user has one of the required roles."""

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            if not current_user or current_user.deleted_at is not None:
                abort(401, description="Invalid or missing authentication token.")
            if not any(current_user.role == role for role in required_roles if role != "self"):
                if "self" in required_roles:
                    user_id = kwargs.get("user_id")
                    if user_id and user_id == current_user_id:
                        return f(*args, **kwargs)
                abort(403, description="You do not have permission to access this resource.")
            return f(*args, **kwargs)
        return wrapper
    return decorator