"""Definitions of user resources."""
import base64
from datetime import datetime
from uuid import uuid4
from bcrypt import gensalt, hashpw
from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.user import AdminUser, EditorUser, RegularUser, User, UserSchema, RegularUserSchema, EditorUserSchema, AdminUserSchema
from ..extensions import DB as db
from ..utils.api_response import SuccessResponse, ErrorResponse
from ..utils.decorators import roles_required

USER_SCHEMA = UserSchema()
USERS_SCHEMA = UserSchema(many=True)

USER_CLASSES = {
    'regular': RegularUser,
    'admin': AdminUser,
    'editor': EditorUser
}

USER_SCHEMAS = {
    'regular': RegularUserSchema(),
    'admin': AdminUserSchema(),
    'editor': EditorUserSchema()
}

class UserListResource(Resource):
    """Resource to handle listing users (admin only)."""

    @jwt_required()
    @roles_required("admin")
    def get(self):
        """Get a list of all users (admin only)."""
        users = User.query.filter(User.deleted_at.is_(None)).all()
        response = SuccessResponse(data=USERS_SCHEMA.dump(users))
        return response.to_dict(), 200
    
    @jwt_required()
    @roles_required("admin")
    def post(self):
        """Create a new user (admin only)."""
        data = request.get_json()
        if User.query.filter_by(username=data['username']).first():
            response = ErrorResponse(message='User already exists')
            return response.to_dict(), 400
        password_bytes = data['password'].encode('utf-8')
        hashed_password = hashpw(password_bytes, gensalt())
        hashed_password_str = base64.b64encode(hashed_password).decode('utf-8')
        role = data.get('role', 'regular').lower()
        UserClass = USER_CLASSES.get(role, RegularUser)
        new_user = UserClass(
            username=data['username'],
            first_name=data['first_name'],
            middle_name=data.get('middle_name', ''),
            last_name=data['last_name'],
            email=data['email'],
            phone_number=data.get('phone_number', ''),
            password_hash=hashed_password_str,
        )
        new_user.id = str(uuid4())
        db.session.add(new_user)
        db.session.commit()
        user_schema = USER_SCHEMAS.get(role, RegularUserSchema())
        response = SuccessResponse(data=user_schema.dump(new_user))
        return response.to_dict(), 201

class UserResource(Resource):
    """Resource to handle user operations (admin only)."""

    @jwt_required()
    @roles_required("admin", "self") 
    def get(self, user_id):
        """Get a user by ID (admin and the user only)."""
        user = User.query.filter(User.deleted_at.is_(None), User.id == user_id).first()
        if not user:
            response = ErrorResponse(message='User not found')
            return response.to_dict(), 404
        response = SuccessResponse(data=USER_SCHEMA.dump(user))
        return response.to_dict(), 200

    @jwt_required()
    @roles_required("admin", "self")
    def delete(self, user_id):
        """Delete a user by ID (admin only)."""
        user_to_delete = User.query.filter(User.deleted_at.is_(None), User.id == user_id).first()
        if not user_to_delete:
            response = ErrorResponse(message='User not found')
            return response.to_dict(), 404
        if user_to_delete.role == 'admin':
            response = ErrorResponse(message='You cannot delete an admin user')
            return response.to_dict(), 400
        user_to_delete.deleted_at = datetime.now()
        db.session.commit()
        response = SuccessResponse(message='User deleted successfully')
        return response.to_dict(), 200

    @jwt_required()
    @roles_required("admin")
    def put(self, user_id):
        """Promote a user to admin (admin only)."""
        user_to_modify = User.query.filter(User.deleted_at.is_(None), User.id == user_id).first()
        if not user_to_modify:
            response = ErrorResponse(message='User not found')
            return response.to_dict(), 404
        if user_to_modify.role == 'admin':
            response = ErrorResponse(message='User is already an admin')
            return response.to_dict(), 400
        data = request.get_json()
        if 'role' in data and data['role'].lower() in ['admin', 'editor', 'regular']:
            user_to_modify.updated_at = datetime.now()
            user_to_modify.role = data['role'].lower()
            db.session.commit()
            response = SuccessResponse(data=USER_SCHEMA.dump(user_to_modify), message='User role updated successfully')
            return response.to_dict(), 200
        else:
            response = ErrorResponse(message='Invalid role specified')
            return response.to_dict(), 400
