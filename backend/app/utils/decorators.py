"""Custom decorators for role-based access control."""
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask import abort
from ..models.user import User, UserRole
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
            if current_user.role not in required_roles and "self" not in required_roles:
                abort(403, description="You do not have permission to access this resource.")
            if "self" in required_roles:
                user_id = kwargs.get("user_id", None)
                print(args)
                if user_id and user_id != current_user_id:
                    abort(403, description="You do not have permission to access this resource")
            return f(*args, **kwargs)
        return wrapper
    return decorator