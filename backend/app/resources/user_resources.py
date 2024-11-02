"""Definitions of user resources."""
import base64
from datetime import datetime
from uuid import uuid4
from bcrypt import gensalt, hashpw
from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.user import User, UserRole, UserSchema, db

USER_SCHEMA = UserSchema()
USERS_SCHEMA = UserSchema(many=True)

class UserListResource(Resource):
    """Resource to handle listing users (admin only)."""

    @jwt_required()
    def get(self):
        """Get a list of all users (admin only)."""
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        if current_user.role != UserRole.ADMIN:
            return {'message': 'You do not have permission to view users.'}, 403
        users = User.query.filter(User.deleted_at.is_(None)).all()
        return {'users': USERS_SCHEMA.dump(users)}, 200
    
    @jwt_required()
    def post(self):
        """Create a new user (admin only)."""
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        if current_user.role != UserRole.ADMIN:
            return {'message': 'You do not have permission to create users.'}, 403
        data = request.get_json()
        password_bytes = data['password'].encode('utf-8')
        hashed_password = hashpw(password_bytes, gensalt())
        hashed_password_str = base64.b64encode(hashed_password).decode('utf-8')
        new_user = User(
            username=data['username'],
            first_name=data['first_name'],
            middle_name=data.get('middle_name', ''),
            last_name=data['last_name'],
            email=data['email'],
            phone_number=data.get('phone_number', ''),
            password_hash=hashed_password_str,
        )
        new_user.id = str(uuid4())
        new_user.role = data.get('role', UserRole.REGULAR)
        db.session.add(new_user)
        db.session.commit()
        return USER_SCHEMA.dump(new_user), 201

class UserResource(Resource):
    """Resource to handle user operations (admin only)."""

    @jwt_required()
    def get(self, user_id):
        """Get a user by ID (admin and the user only)."""
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        if current_user.role != UserRole.ADMIN and current_user_id != user_id:
            return {'message': 'You do not have permission to view user.'}, 403
        user = User.query.filter(User.deleted_at.is_(None), User.id == user_id).first()
        if not user:
            return {'message': 'User not found'}, 404
        return USER_SCHEMA.dump(user), 200

    @jwt_required()
    def delete(self, user_id):
        """Delete a user by ID (admin only)."""
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        if current_user.role != UserRole.ADMIN and current_user_id != user_id:
            return {'message': 'You do not have permission to delete users.'}, 403
        user_to_delete = User.query.filter(User.deleted_at.is_(None), User.id == user_id).first()
        if not user_to_delete:
            return {'message': 'User not found'}, 404
        if user_to_delete.role == UserRole.ADMIN:
            return {'message': 'You cannot delete an admin user.'}, 400
        user_to_delete.deleted_at = datetime.now()
        db.session.commit()
        return {'message': 'User deleted successfully.'}, 200

    @jwt_required()
    def put(self, user_id):
        """Promote a user to admin (admin only)."""
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        if current_user.role != UserRole.ADMIN:
            return {'message': 'You do not have permission to modify users.'}, 403
        user_to_modify = User.query.filter(User.deleted_at.is_(None), User.id == user_id).first()
        if not user_to_modify:
            return {'message': 'User not found'}, 404
        if user_to_modify.role == UserRole.ADMIN:
            return {'message': 'User is already an admin.'}, 400
        data = request.get_json()
        if 'role' in data and data['role'] in [role.value for role in UserRole]:
            print(data)
            user_to_modify.updated_at = datetime.now()
            user_to_modify.role = data['role']
            db.session.commit()
            return {'message': f"User role updated to {data['role']}."}, 200
        else:
            return {'message': 'Invalid role specified.'}, 400
