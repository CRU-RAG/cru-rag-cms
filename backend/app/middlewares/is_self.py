"""Middleware to check if users are accessing their own data"""
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask import abort
from ..models.user import User

def is_self(f):
    """Decorator to check if users are accessing their own data"""
    @wraps
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        current_user_id = get_jwt_identity()
        request_user_id = kwargs.get('user_id')
        if current_user_id != request_user_id:
            abort(403, description="Access restricted to the user.")
        return wrapper
