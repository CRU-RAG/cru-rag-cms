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
from ..utils.api_response import Response
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
        response = Response(
            data=USERS_SCHEMA.dump(users),
            message='Users retrieved successfully'
        )
        return response.to_dict(), 200
    
    @jwt_required()
    @roles_required("admin")
    def post(self):
        """Create a new user (admin only)."""
        data = request.get_json()
        if User.query.filter_by(username=data['username']).first():
            response = Response(
                message='Unable to create user',
                error='User already exists',
                status=400
            )
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
        response = Response(
            data=user_schema.dump(new_user),
            message='User created successfully',
            status=201
        )
        return response.to_dict(), 201

class UserResource(Resource):
    """Resource to handle user operations (admin only)."""

    @jwt_required()
    @roles_required("admin", "self") 
    def get(self, user_id):
        """Get a user by ID (admin and the user only)."""
        user = User.query.filter(User.deleted_at.is_(None), User.id == user_id).first()
        if not user:
            response = Response(
                message='Unable to retrieve user',
                error='User not found',
                status=404
            )
            return response.to_dict(), 404
        response = Response(
            data=USER_SCHEMA.dump(user),
            message='User retrieved successfully',
        )
        return response.to_dict(), 200

    @jwt_required()
    @roles_required("admin", "self")
    def delete(self, user_id):
        """Delete a user by ID (admin only)."""
        user_to_delete = User.query.filter(User.deleted_at.is_(None), User.id == user_id).first()
        if not user_to_delete:
            response = Response(
                message='Unable to delete user',
                error='User not found',
                status=404
            )
            return response.to_dict(), 404
        if user_to_delete.role == 'admin':
            response = Response(
                message='Unable to delete user',
                error='The user is an admin',
                status=400
            )
            return response.to_dict(), 400
        user_to_delete.deleted_at = datetime.now()
        db.session.commit()
        response = Response(
            message='User deleted successfully',
        )
        return response.to_dict(), 200

    @jwt_required()
    @roles_required("admin")
    def put(self, user_id):
        """Promote a user to admin (admin only)."""
        user_to_modify = User.query.filter(User.deleted_at.is_(None), User.id == user_id).first()
        if not user_to_modify:
            response = Response(
                message='Unable to update user role',
                error='User not found',
                status=404
            )
            return response.to_dict(), 404
        if user_to_modify.role == 'admin':
            response = Response(
                message='Unable to update user role',
                error='User is an admin',
                status=400
            )
            return response.to_dict(), 400
        data = request.get_json()
        if 'role' in data and data['role'].lower() in ['admin', 'editor', 'regular']:
            user_to_modify.updated_at = datetime.now()
            user_to_modify.role = data['role'].lower()
            db.session.commit()
            response = Response(
                data=USER_SCHEMA.dump(user_to_modify), 
                message='User role updated successfully'
            )
            return response.to_dict(), 200
        else:
            response = Response(
                message='Unable to update user role',
                error='Invalid role',
                status=400
            )
            return response.to_dict(), 400
